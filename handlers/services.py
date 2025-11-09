"""Conversation handlers for the service request bot."""
import logging
import re
from email.message import EmailMessage
from typing import Optional
from urllib.parse import quote

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import CallbackQuery, InputFile, ReplyKeyboardRemove
from asgiref.sync import sync_to_async

from config import settings
from handlers.states import AuthState
from keyboards.choise_buttons import (
    build_confirmation_keyboard,
    build_contract_keyboard,
    build_payment_keyboard,
    build_plan_keyboard,
    build_skip_keyboard,
    get_service_keyboard,
    get_social_network_keyboard,
)
from loader import bot, dp
from service_catalog import SERVICE_OPTIONS, ServiceOption, SubscriptionPlan, resolve_service_option, resolve_social_network

logger = logging.getLogger(__name__)

PHONE_SANITIZE_PATTERN = re.compile(r"[\s()-]")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
SKIP_WORDS = {"пропустить", "skip", "no", "нет"}


def format_price(price: int) -> str:
    return f"{price:,}".replace(",", " ")


def get_service_by_code(code: str) -> ServiceOption:
    for option in SERVICE_OPTIONS:
        if option.code == code:
            return option
    raise ValueError(f"Unknown service code: {code}")


def get_plan_by_code(service: ServiceOption, plan_code: str) -> Optional[SubscriptionPlan]:
    for plan in service.subscription_plans:
        if plan.code == plan_code:
            return plan
    return None


def get_description(price: int, service: str, target: str) -> str:
    raw_description = settings.payment_description_template.format(
        price=format_price(price), service=service, target=target
    )
    return quote(raw_description, safe="/")


def make_hash(price: int, phone: str, telegram_id: int) -> str:
    payload = (
        f"{settings.robokassa_merchant_login}:{price}:0:{settings.robokassa_password1}:"
        f"Shp_phone={phone}:Shp_telegram={telegram_id}"
    )
    import hashlib

    return hashlib.md5(payload.encode("utf-8")).hexdigest()


@sync_to_async
def make_link(data: dict) -> str:
    phone = data["phone"]
    telegram_id = data["telegram_id"]
    service = data["service"]
    social_net = data["social_net"]
    link = data["link"]
    plan = data.get("subscription_plan")
    price = data["price"]
    target = f"{social_net}: {link}"
    if plan:
        target = f"{target} ({plan})"
    md5 = make_hash(price, phone, telegram_id)
    description = get_description(price, service, target)
    return (
        f"{settings.robokassa_base_url}?MerchantLogin={settings.robokassa_merchant_login}&InvId=0&Culture=ru&Encoding=utf-8"
        f"&Shp_phone={phone}&Shp_telegram={telegram_id}&OutSum={price}&Description={description}&SignatureValue={md5}"
    )


@sync_to_async
def post_data_to_email(data: dict) -> bool:
    recipients = settings.email_recipients
    if not recipients:
        logger.warning("No email recipients configured; skipping notification.")
        return False

    message_lines = [
        "Получена новая заявка из Telegram-бота IST-detector.",
        "",
        f"Пользователь: {data.get('username', '—')}",
        f"Telegram ID: {data.get('telegram_id')}",
        f"Социальная сеть/объект: {data.get('social_net')}",
        f"Ссылка или идентификатор: {data.get('link')}",
        f"Услуга: {data.get('service')}",
        f"Стоимость: {format_price(data.get('price'))} руб.",
    ]
    if data.get("subscription_plan"):
        message_lines.append(f"Тариф: {data['subscription_plan']}")
    message_lines.append(f"Телефон: {data.get('phone')}")
    if data.get("email"):
        message_lines.append(f"Email: {data['email']}")
    if data.get("comment"):
        message_lines.append("Комментарий:")
        message_lines.append(data["comment"])
    if data.get("payment_link"):
        message_lines.extend(["", f"Ссылка для оплаты: {data['payment_link']}"])
    body = "\n".join(message_lines)

    email_message = EmailMessage()
    email_message["Subject"] = "Новая заявка из Telegram-бота IST-detector"
    email_message["From"] = settings.email_from
    email_message.set_content(body)

    import smtplib

    try:
        with smtplib.SMTP_SSL(settings.email_host) as server:
            server.login(settings.email_from, settings.email_password)
            for recipient in recipients:
                email_message["To"] = recipient
                server.send_message(email_message)
                del email_message["To"]
    except Exception as exc:  # pragma: no cover - network errors are environment specific
        logger.exception("Failed to send notification email: %s", exc)
        return False
    return True


@dp.message_handler(Command("start"))
async def answer(message: types.Message, state: FSMContext):
    await state.finish()
    username = message.from_user.full_name
    telegram_id = message.from_user.id
    await AuthState.social_net.set()
    image = InputFile(path_or_bytesio="handlers/images/im.png")
    greeting = (
        f"Здравствуйте, {username} 👋\n\n"
        "📱 IST-detector поможет решить вопросы в сфере защиты данных. "
        "Я могу провести тестирование Ваших аккаунтов на возможность взлома."
    )
    await bot.send_photo(telegram_id, image, caption=greeting)
    await message.answer(
        "С какой из систем будем работать?",
        reply_markup=get_social_network_keyboard(),
    )


@dp.message_handler(Command("help"), state="*")
async def help_command(message: types.Message):
    await message.answer(
        "Я помогу оформить заявку на проверку безопасности аккаунтов. "
        "Используйте /start, чтобы начать заново, /services, чтобы увидеть список услуг, и /cancel, чтобы прервать диалог."
    )


@dp.message_handler(Command("services"), state="*")
async def services_command(message: types.Message):
    services = "\n".join(f"• {option.label}" for option in SERVICE_OPTIONS)
    await message.answer(
        "Доступные услуги:\n" + services,
        reply_markup=get_service_keyboard(),
    )


@dp.message_handler(Command("cancel"), state="*")
async def cancel_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Диалог прерван. Чтобы начать заново, используйте /start.", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=AuthState.social_net)
async def get_social(message: types.Message, state: FSMContext):
    social_net = resolve_social_network(message.text)
    if not social_net:
        await message.answer("Выберите объект из предложенных в клавиатуре.")
        return
    await state.update_data(social_net=social_net.label)
    await AuthState.next()
    default_text = (
        f"Проверьте свой аккаунт {social_net.label} на попытки взлома 🔓\n\n"
        "Узнайте, кто хотел получить доступ к Вашим сообщениям, фотографиям и спискам друзей 🔎\n\n"
        "Получите информацию о рисках утечки данных и включите мониторинг, чтобы мы могли предупреждать Вас об инцидентах."
    )
    if social_net.code.startswith("web"):
        default_text = (
            "Проверьте свой сайт на попытки взлома 🔓\n\n"
            "Получите исчерпывающую информацию о рисках утечки данных и настройте мониторинг безопасности."
        )
    await message.answer(default_text, reply_markup=get_service_keyboard())


@dp.message_handler(state=AuthState.service)
async def get_service(message: types.Message, state: FSMContext):
    service = resolve_service_option(message.text)
    if not service:
        await message.answer("Выберите услугу из предложенных в клавиатуре.")
        return
    await state.update_data(service=service.label, service_code=service.code)
    await message.answer(service.description, reply_markup=ReplyKeyboardRemove())
    await message.answer(
        "Укажите Ваш аккаунт (ссылку на него, ID, логин) 👤",
    )
    await AuthState.next()


@dp.message_handler(state=AuthState.link)
async def get_link(message: types.Message, state: FSMContext):
    link = message.text.strip()
    await state.update_data(link=link)
    data = await state.get_data()
    service = get_service_by_code(data["service_code"])
    if service.requires_plan():
        await AuthState.plan.set()
        await message.answer(
            "Выберите периодичность мониторинга:",
            reply_markup=build_plan_keyboard(service.subscription_plans),
        )
    else:
        await prepare_for_phone(message, state, service, service.price)


async def prepare_for_phone(
    message: types.Message, state: FSMContext, service: ServiceOption, price: int, plan: Optional[SubscriptionPlan] = None
) -> None:
    await state.update_data(price=price)
    if plan:
        await state.update_data(subscription_plan=plan.label)
        await message.answer(f"Выбран тариф: {plan.label}\n{plan.description}")
    else:
        await state.update_data(subscription_plan=None)
    await message.answer(f"Стоимость услуги: {format_price(price)} руб.")
    await message.answer(service.payment_hint)
    await message.answer(service.phone_prompt, reply_markup=ReplyKeyboardRemove())
    await AuthState.phone.set()


@dp.callback_query_handler(Text(startswith="plan:"), state=AuthState.plan)
async def select_plan(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    data = await state.get_data()
    service = get_service_by_code(data["service_code"])
    plan_code = call.data.split(":", 1)[1]
    plan = get_plan_by_code(service, plan_code)
    if not plan:
        await call.message.answer("Не удалось определить тариф. Пожалуйста, выберите вариант из списка.")
        return
    await call.message.edit_reply_markup()
    await prepare_for_phone(call.message, state, service, plan.price, plan)


@dp.message_handler(state=AuthState.phone)
async def get_phone(message: types.Message, state: FSMContext):
    cleaned = PHONE_SANITIZE_PATTERN.sub("", message.text.strip())
    if cleaned.startswith("+"):
        digits = cleaned[1:]
    else:
        digits = cleaned
    if not digits.isdigit() or len(digits) < 6:
        await message.answer("Неверный формат номера ⚠. Пожалуйста, отправьте номер цифрами.")
        return
    normalised = "+" + digits if cleaned.startswith("+") else digits
    await state.update_data(phone=normalised)
    await AuthState.email.set()
    await message.answer(
        "Оставьте e-mail для связи (или отправьте 'Пропустить').",
        reply_markup=build_skip_keyboard(),
    )


@dp.message_handler(state=AuthState.email)
async def get_email(message: types.Message, state: FSMContext):
    text = message.text.strip()
    if text.lower() in SKIP_WORDS:
        await state.update_data(email=None)
    elif EMAIL_PATTERN.match(text):
        await state.update_data(email=text)
    else:
        await message.answer("Похоже, адрес некорректен. Попробуйте снова или отправьте 'Пропустить'.")
        return
    await AuthState.comment.set()
    await message.answer(
        "Если есть дополнительные сведения, напишите их (или отправьте 'Пропустить').",
        reply_markup=build_skip_keyboard(),
    )


@dp.message_handler(state=AuthState.comment)
async def get_comment(message: types.Message, state: FSMContext):
    text = message.text.strip()
    if text.lower() in SKIP_WORDS:
        await state.update_data(comment=None)
    else:
        await state.update_data(comment=text)
    await send_confirmation(message, state)


async def send_confirmation(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    service = get_service_by_code(data["service_code"])
    summary_lines = [
        "Проверьте, пожалуйста, данные заявки:",
        f"• Социальная сеть: {data.get('social_net')}",
        f"• Ссылка/логин: {data.get('link')}",
        f"• Услуга: {service.label}",
        f"• Стоимость: {format_price(data.get('price'))} руб.",
        f"• Телефон: {data.get('phone')}",
    ]
    if data.get("subscription_plan"):
        summary_lines.insert(4, f"• Тариф: {data['subscription_plan']}")
    if data.get("email"):
        summary_lines.append(f"• Email: {data['email']}")
    if data.get("comment"):
        summary_lines.append(f"• Комментарий: {data['comment']}")
    await AuthState.confirmation.set()
    await message.answer(
        "\n".join(summary_lines),
        reply_markup=build_confirmation_keyboard(),
    )


@dp.callback_query_handler(Text(equals="confirm_request"), state=AuthState.confirmation)
async def confirm_request(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    telegram_id = call.from_user.id
    data.setdefault("telegram_id", telegram_id)
    data.setdefault("username", call.from_user.full_name)
    payment_link = await make_link(data)
    await state.update_data(payment_link=payment_link)
    await call.message.edit_reply_markup()
    await call.message.answer(
        "Вы можете оплатить заказ через Робокассу по ссылке ниже:",
        reply_markup=build_payment_keyboard(payment_link),
    )
    await call.message.answer(
        "Отчет о работе будет направлен в этот Telegram. Также доступен договор и реквизиты:",
        reply_markup=build_contract_keyboard(),
    )
    email_sent = await post_data_to_email(await state.get_data())
    if email_sent:
        await call.message.answer("Заявка отправлена. Мы свяжемся с Вами в ближайшее время!")
    else:
        await call.message.answer(
            "Не удалось автоматически отправить уведомление по e-mail. Мы проверим заявку вручную."
        )
    await state.finish()


@dp.callback_query_handler(Text(equals="cancel_request"), state=AuthState.confirmation)
async def cancel_request(call: CallbackQuery, state: FSMContext):
    await call.answer("Заявка отменена")
    await call.message.edit_reply_markup()
    await state.finish()
    await call.message.answer("Заявка отменена. Используйте /start, чтобы начать заново.")
