from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from botish.bot.texts import Texts, PERIODS, CBK_DATA_PERIOD_UP


def start_kb() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text=Texts.settings)],
    ]

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        is_persistent=True,
    )


def settings_kb() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text=Texts.period_up), KeyboardButton(text=Texts.period_down)],
        [
            KeyboardButton(text=Texts.percent_up),
            KeyboardButton(text=Texts.percent_down),
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def period_up_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text=p, callback_data=f"{CBK_DATA_PERIOD_UP}{p}")
            for p in PERIODS
        ],
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
