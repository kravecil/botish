from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from botish.bot.texts import ButtonCaption
from aiogram.types import Message
from botish.user import User
from botish.bot.keyboards import settings_kb

router = Router()


class PercentStates(StatesGroup):
    up = State()
    down = State()


@router.message(F.text == ButtonCaption.percent_up)
async def percent_up_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Введите процент роста (целое число от 1 до 100):",
    )
    await state.set_state(PercentStates.up)


@router.message(F.text == ButtonCaption.percent_down)
async def percent_down_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Введите процент просадки (целое число от 1 до 100):",
    )
    await state.set_state(PercentStates.down)


@router.message(PercentStates.up)
async def percent_up_value_handler(message: Message, state: FSMContext) -> None:
    try:
        await _set_percent_setting(message, is_up=True)

        await state.clear()

    except ValueError:
        await message.answer("Ошибка: введите корректное число.")


@router.message(PercentStates.down)
async def percent_down_value_handler(message: Message, state: FSMContext) -> None:
    try:
        await _set_percent_setting(message, is_up=False)

        await state.clear()

    except ValueError:
        await message.answer("Ошибка: введите корректное число.")


async def _set_percent_setting(message: Message, *, is_up: bool):
    if not message.text:
        await message.answer("Ошибка: необходимо ввести целое число.")
        return

    percent = int(message.text)

    if not (1 <= percent <= 100):
        await message.answer("Ошибка: введите целое число от 1 до 100.")
        return

    user = await User.get(message.chat.id)

    if is_up:
        await user.update_percent_up(percent)

        await message.answer(
            f"Процент роста установлен: {percent}",
            reply_markup=settings_kb(),
        )
    else:
        await user.update_percent_down(percent)

        await message.answer(
            f"Процент просадки установлен: {percent}",
            reply_markup=settings_kb(),
        )
