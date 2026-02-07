from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from botish.bot.texts import (
    ButtonCaption,
    PERIODS,
    CLBK_SETTINGS_CHANGED,
    SettingsCallback,
)


def start_kb() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text=ButtonCaption.settings)],
    ]

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        is_persistent=True,
    )


def settings_kb() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text=ButtonCaption.period_up),
            KeyboardButton(text=ButtonCaption.period_down),
        ],
        [
            KeyboardButton(text=ButtonCaption.percent_up),
            KeyboardButton(text=ButtonCaption.percent_down),
        ],
        [
            KeyboardButton(text=ButtonCaption.back_to_settings),
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
            InlineKeyboardButton(
                text=p,
                callback_data=f"{CLBK_SETTINGS_CHANGED}:{SettingsCallback.period_up}:{p}",
            )
            for p in PERIODS
        ],
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )


def period_down_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=p,
                callback_data=f"{CLBK_SETTINGS_CHANGED}:{SettingsCallback.period_down}:{p}",
            )
            for p in PERIODS
        ],
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
