from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loader import dp, bot
from .states import AuthState
from aiogram.dispatcher.filters import Command
from keyboards.choise_buttons import choise, choise2, accoun, choise3, button_3000, button_300, button_30000, button_change
from asgiref.sync import sync_to_async
import hashlib
from urllib.parse import quote
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from config import EMAIL_PASSWORD, HOST, EMAIL_FROM, EMAIL_TO_1, EMAIL_TO_2, EMAIL_TO_3, EMAIL_TO_4
import re


def get_description(price, service, net):
    if price == 30000:
        price = '30 000'
    description = f'Оплата {price}руб за оказание услуги: "{service}", объект для проверки: {net} '
    result = quote(description, safe='/')
    return result


def make_hash(price, phone, telegram_id):
    hash_obj = hashlib.md5(f"infsectest_ru:{price}:0:qNI1cl89rPWbFMkb9Ls0:Shp_phone={phone}:Shp_telegram={telegram_id}".encode())
    return hash_obj.hexdigest()


@sync_to_async
def post_data_to_email(data, HOST=HOST, FROM=EMAIL_FROM, TO=[EMAIL_TO_1, EMAIL_TO_2, EMAIL_TO_3, EMAIL_TO_4], PASSWORD=EMAIL_PASSWORD):
    try:
        phone=data['phone']
        telegram_id=data['telegram_id']
        service=data['service']
        social_net=data['social_net']
        link=data['link']
        final_price = data['price']
    except KeyError as ke:
        return ke
    SUBJECT = f"Заказ\nУслуга: {service}\nСоциальная сеть:{social_net}, ссылка: {link}\nТелефон: {phone}\nЦена: {final_price}\ntelegram_id: {telegram_id}"
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Заказ"
    msg['From'] = FROM
    for mail in TO:
        msg['To'] = mail
        body = MIMEText(SUBJECT)
        msg.attach(body)
        username = FROM
        PASSWORD = PASSWORD
        try:
            try:
                server = smtplib.SMTP_SSL(HOST)
            except:
                return 990
            try:
                server.login(username, PASSWORD)
            except:
                return 998
            try:
                server.sendmail(FROM, mail, msg.as_string())
            except:
                return 100000
            server.quit()
        except Exception:
            return 400
    return True


@sync_to_async
def make_link(data):
    phone=data['phone']
    net = data['social_net']
    telegram_id=data['telegram_id']
    service=data['service']
    final_price = data['price']
    md5 = make_hash(final_price, phone, telegram_id)
    description = get_description(final_price, service, net)
    link_to_pay = f"https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=infsectest_ru&InvId=0&Culture=ru&Encoding=utf-8&Shp_phone={phone}&Shp_telegram={telegram_id}&OutSum={final_price}&Description={description}&SignatureValue={md5}"
    return link_to_pay


permitted = [
    'анализ рисков безопасности', 'узнать, пытались ли взломать', 'мониторинг', 'расследование', 'анализ утечек'
    ]

nets = ['вконтакте', 'instagram', 'facebook', 'email', 'web-сайты и cms системы',]

dic = {}


@dp.message_handler(Command('start'))
async def answer(message: types.Message):
    username = message.from_user.full_name
    telegram_id = message.from_user.id
    await AuthState.social_net.set()
    image = InputFile(path_or_bytesio='handlers/images/im.png')
    text = f'Здравствуйте, {username} 👋\n\n 📱 IST-detector может помочь решить Вам большинство вопросов в сфере защиты данных, также я могу провести тестирование Ваших аккаунтов на возможность взлома'
    await bot.send_photo(telegram_id, image, caption=text)
    await message.answer('С какой из систем будем работать?', reply_markup=choise2)


@dp.message_handler(state=AuthState.social_net)
async def get_social(message: types.Message, state: FSMContext):
    social_net = message.text
    if not social_net.lower() in nets:
        await message.answer('Выберите тестируемый объект из предложенных')
        return
    await state.update_data(social_net=social_net)
    if social_net.lower() == 'web-сайты и cms системы':
        await message.answer('Проверьте свой сайт на попытки взлома 🔓\n\n '\
                        'Узнайте, кто хотел получить доступ к Вашим сообщениям, фотографиям и спискам друзей 🔎\n\n Получите исчерпывающую информацию 📂 о рисках утечки данных, об общих рисках для безопасности данных и включите мониторинг ИБ, чтобы мы могли предупреждать ⚠️  Вас обо всех инцидентах, фиксируемых нашим центром информационной безопасности.', reply_markup=choise)
    else:
        await message.answer(f'Проверьте свой аккаунт {social_net} на попытки взлома 🔓\n\n '\
                        'Узнайте, кто хотел получить доступ к Вашим сообщениям, фотографиям и спискам друзей 🔎\n\n Получите исчерпывающую информацию 📂 о рисках утечки данных, об общих рисках для безопасности данных и включите мониторинг ИБ, чтобы мы могли предупреждать ⚠️  Вас обо всех инцидентах, фиксируемых нашим центром информационной безопасности.', reply_markup=choise)
    await AuthState.next()


@dp.message_handler(state=AuthState.service)
async def get_service(message: types.Message, state: FSMContext):
    service = message.text
    if not service.lower() in permitted:
        await message.answer('Выберите услугу из предложенных')
        return
    await state.update_data(service=service)
    await message.answer('Укажите Ваш аккаунт (ссылку на него, id, логин) 👤', reply_markup=types.ReplyKeyboardRemove())
    await AuthState.next()


@dp.message_handler(state=AuthState.link)
async def get_link(message: types.Message, state: FSMContext):
    link = message.text
    await state.update_data(link=link)
    data = await state.get_data()
    telegram_id = int(message.from_user.id)
    dic.setdefault(telegram_id, data)
    service = data['service']
    await state.finish()
    if service.lower() == 'узнать, пытались ли взломать':
        await message.answer('Я помогу узнать, заказывали ли взлом Вашего аккаунта в Darknet или у профессиональных хакеров 🖥. Предоставлю Вам информацию по целевым атакам, их датам и успешности')
        await AuthState.price.set()
        await state.update_data(price=3000)
        await AuthState.next()
        await message.answer('Оплата осуществляется через авторизованный сервис Робокасса, являющийся одним из ведущих в РФ, что гарантирует безопасность платежей ⚒')
        await message.answer('Введите номер телефона ☎️ привязанный к выбранному аккаунту.')


    elif service.lower() == 'анализ рисков безопасности':
        await message.answer('Будет произведен анализ Вашего аккаунта на возможные риски несанкционированного доступа 🗝')
        await AuthState.price.set()
        await state.update_data(price=300)
        await AuthState.next()
        await message.answer('Оплата осуществляется через авторизованный сервис Робокасса, являющийся одним из ведущих в РФ, что гарантирует безопасность платежей ⚒')
        await message.answer('Введите номер телефона ☎️ привязанный к выбранному аккаунту')


    elif service.lower() == 'анализ утечек':
        await message.answer('Проверьте взламывали ли Ваш аккаунт и есть ли риск утечки данных')
        await AuthState.price.set()
        await state.update_data(price=300)
        await AuthState.next()
        await message.answer('Оплата осуществляется через авторизованный сервис Робокасса, являющийся одним из ведущих в РФ, что гарантирует безопасность платежей ⚒')  
        await message.answer('Введите номер телефона ☎️ привязанный к выбранному аккаунту')


    elif service.lower() == 'мониторинг':
        await message.answer(text='Укажите периодичность мониторинга информационной безопасности Вашего аккаунта и оплатите услугу. Отчеты будут предоставляться на Ваш Telegram в формате Secret Chat. Первый отчет через 2 дня после заказа 👇', reply_markup=button_change)

    elif service.lower() == 'расследование':
        await message.answer('Если у Вас произошел инцидент несанкционированного доступа 🕷 в аккаунт. Мы можем помочь найти злоумышленника. Гарантируем предоставить расширенные сведения об инциденте, которые помогут Вам понять, в чем причина и кто мог быть Заказчиком. В каждом втором случае мы устанавливаем конечного Заказчика. В одном из трех случаев нам с точностью удается установить и Исполнителя, и Заказчика. В одном из десяти случаев собрать доказательную базу 📁')
        await AuthState.price.set()
        await state.update_data(price=30000)
        await AuthState.next()
        await message.answer('Оплата осуществляется через авторизованный сервис Робокасса, являющийся одним из ведущих в РФ, что гарантирует безопасность платежей ⚒')
        await message.answer('Введите номер телефона ☎️ привязанный к выбранному аккаунту')


@dp.callback_query_handler(text_contains='choise250')
async def del_keywords(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await AuthState.price.set()
    await call.message.answer('Введите номер телефона ☎️ привязанный к выбранному аккаунту')
    await state.update_data(price=250)
    await AuthState.next()


@dp.callback_query_handler(text_contains='choise800')
async def del_keywords(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await AuthState.price.set()
    await call.message.answer('Введите номер телефона ☎️ привязанный к выбранному аккаунту')
    await state.update_data(price=800)
    await AuthState.next()


@dp.callback_query_handler(text_contains='choise4500')
async def del_keywords(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await AuthState.price.set()
    await call.message.answer('Введите номер телефона ☎️ привязанный к выбранному аккаунту')
    await state.update_data(price=4500)
    await AuthState.next()


@dp.message_handler(state=AuthState.phone)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.text
    try:
        phone = int(phone)
    except ValueError:
        await message.answer('Неверный формат номера ⚠')
        return
    if len(str(phone)) < 6:
        await message.answer('Неверный формат номера ⚠')
        return
    await state.update_data(phone=phone)
    telegram_id = int(message.from_user.id)
    data = await state.get_data()
    data.setdefault('telegram_id', telegram_id)
    for key, value in data.items():
        dic[telegram_id].setdefault(key, value)
    link = await make_link(dic[telegram_id])
    await state.finish()
    button_link = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Оплатить через Робокассу ', url=link))
    await message.answer('Вы можете осуществить оплату через авторизованный сервис Телеграмм (выше) или через внешний сервис Робокасса, один из ведущих в РФ 💳', reply_markup=button_link)
    button_recv = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Договор, реквизиты ', url='https://infsectest.ru/docs/offer.pdf'))
    await message.answer('Отчет о проведенной работе будет направлен Вам в телеграмм, с которого осуществлялся заказ 📋\n\n Отправляем Вам также ссылку на договор оказания услуг, где Вы сможете ознакомиться с гарантиями и обязательствами Российского юридического лица, существующего более 15 лет на рынке. Там же Вы найдете наши официальные реквизиты 👇', reply_markup=button_recv)
    responce = await post_data_to_email(dic[telegram_id])
    dic.pop(telegram_id)


