from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from botish.bot.keyboards import period_up_kb, settings_kb, start_kb
from botish.bot.texts import CBK_DATA_PERIOD_UP, PERIODS, Texts
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


@router.message(F.text == Texts.settings)
async def command_settings_handler(message: Message) -> None:
    user = await User.get(message.chat.id)

    settings = user.settings

    reply_text = (
        "📈<b>Рост</b>\n"
        f"период {settings.open_interest.period_up or Texts.settings_null}\n"
        f"процент {settings.open_interest.percent_up or Texts.settings_null}\n"
        "\n"
        "📉<b>Просадка</b>\n"
        f"период {settings.open_interest.period_down or Texts.settings_null}\n"
        f"процент {settings.open_interest.percent_down or Texts.settings_null}\n"
    )

    await message.answer(
        f"<u>Ваши текущие настройки:</u>\n\n{reply_text}", reply_markup=settings_kb()
    )


@router.message(F.text == Texts.period_up)
async def command_period_up_handler(message: Message) -> None:
    await message.answer(
        "Выберите период роста (в минутах):", reply_markup=period_up_kb()
    )


@router.callback_query(F.data.startswith(CBK_DATA_PERIOD_UP))
async def callback_period_up(call: CallbackQuery) -> None:
    await call.answer()

    if not call.data:
        return

    if call.message is not None:
        period_up_key = call.data.replace(CBK_DATA_PERIOD_UP, "")
        period_up_value = PERIODS[period_up_key]

        user = await User.get(call.message.chat.id)
        await user.update_period_up(period_up_value)

        await call.message.answer(
            f"Период роста установлен: {period_up_key}", reply_markup=settings_kb()
        )
