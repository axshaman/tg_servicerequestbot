"""Keyboard builders for the service request flow."""
from typing import Iterable

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from service_catalog import SERVICE_OPTIONS, SOCIAL_NETWORKS, SubscriptionPlan


def _chunk(buttons: Iterable[KeyboardButton], row_size: int) -> Iterable[list[KeyboardButton]]:
    buttons = list(buttons)
    for index in range(0, len(buttons), row_size):
        yield buttons[index : index + row_size]


def get_social_network_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_rows = _chunk((KeyboardButton(network.label) for network in SOCIAL_NETWORKS), 2)
    for row in button_rows:
        markup.row(*row)
    return markup


def get_service_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_rows = _chunk((KeyboardButton(option.label) for option in SERVICE_OPTIONS), 2)
    for row in button_rows:
        markup.row(*row)
    return markup


def build_plan_keyboard(plans: Iterable[SubscriptionPlan]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    for plan in plans:
        markup.insert(
            InlineKeyboardButton(text=plan.label, callback_data=f"plan:{plan.code}")
        )
    return markup


def build_payment_keyboard(url: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton("Оплатить через Робокассу", url=url))
    return markup


def build_contract_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
        InlineKeyboardButton("Договор, реквизиты", url="https://infsectest.ru/docs/offer.pdf")
    )
    return markup


def build_confirmation_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("Подтвердить", callback_data="confirm_request"))
    markup.add(InlineKeyboardButton("Отменить", callback_data="cancel_request"))
    return markup


def build_skip_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Пропустить"))
    return markup
