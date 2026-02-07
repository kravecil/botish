from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from botish.bot.keyboards import period_up_kb, settings_kb, start_kb
from botish.bot.texts import CLBK_SETTINGS_CHANGED, TXT_SETTINGS_NULL, ButtonCaption
from botish.user import User

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    chat = message.chat
    user = await User.register(
        chat_id=chat.id, username=chat.username, full_name=chat.full_name
    )

    await message.answer(
        "<b><u>Open Interest BOT!</u></b>\n\n"
        f"✨ Здравствуй, <b>{user.full_name}</b>! ✨\n"
        "Ты успешно зарегистрировался в нашем боте! 🎉🎉🎉",
        reply_markup=start_kb(),
    )


@router.message(F.text == ButtonCaption.settings)
async def command_settings_handler(message: Message) -> None:
    user = await User.get(message.chat.id)

    settings = user.settings

    reply_text = (
        "📈<b>Рост</b>\n"
        f"период {settings.open_interest.period_up or TXT_SETTINGS_NULL}\n"
        f"процент {settings.open_interest.percent_up or TXT_SETTINGS_NULL}\n"
        "\n"
        "📉<b>Просадка</b>\n"
        f"период {settings.open_interest.period_down or TXT_SETTINGS_NULL}\n"
        f"процент {settings.open_interest.percent_down or TXT_SETTINGS_NULL}\n"
    )

    await message.answer(
        f"<u>Ваши текущие настройки:</u>\n\n{reply_text}", reply_markup=settings_kb()
    )


@router.message(F.text == ButtonCaption.period_up)
async def command_period_up_handler(message: Message) -> None:
    await message.answer(
        "Выберите период роста (в минутах):", reply_markup=period_up_kb()
    )


@router.callback_query(F.data.startswith(f"{CLBK_SETTINGS_CHANGED}:"))
async def callback_settings_changed(call: CallbackQuery) -> None:
    await call.answer()

    if not call.data:
        return

    if call.message is not None:
        user = await User.get(call.message.chat.id)

        data = call.data.replace(f"{CLBK_SETTINGS_CHANGED}:", "").split(":")
        setting_key = data[0]
        setting_value = data[1]

        match setting_key:
            case "period_up":
                user = await User.get(call.message.chat.id)
                await user.update_period_up(int(setting_value))

                await call.message.answer(
                    f"Период роста установлен: {setting_key}",
                    reply_markup=settings_kb(),
                )
            case "period_down":
                user = await User.get(call.message.chat.id)
                await user.update_period_down(int(setting_value))

                await call.message.answer(
                    f"Период просадки установлен: {setting_key}",
                    reply_markup=settings_kb(),
                )
