import asyncio
import time
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Bot


class TelegramBotLimiter:
    def __init__(self, max_messages_total: int = 30, user_rate_limit: float = 1.0):
        self.max_messages_total = max_messages_total
        self.user_rate_limit = user_rate_limit

        # Глобальный счётчик сообщений
        self.total_messages_sent = 0
        self.total_messages_lock = asyncio.Lock()

        # Храним последнее время отправки для каждого пользователя
        self.user_last_sent: dict[int, float] = defaultdict(float)
        self.user_lock = asyncio.Lock()

    async def wait_for_user_limit(self, user_id: int):
        """Ожидает, пока не пройдёт 1 секунда с последней отправки пользователю"""
        while True:
            async with self.user_lock:
                last_sent = self.user_last_sent[user_id]
                now = time.time()
                if (now - last_sent) >= self.user_rate_limit:
                    # Обновляем время сразу при получении «окна»
                    self.user_last_sent[user_id] = now
                    return
            # Ждём остаток времени до следующего разрешённого момента
            wait_time = self.user_rate_limit - (now - last_sent)
            await asyncio.sleep(wait_time)

    async def wait_for_global_limit(self):
        """Ожидает, пока не освободится место в глобальном лимите"""
        while True:
            async with self.total_messages_lock:
                if self.total_messages_sent < self.max_messages_total:
                    self.total_messages_sent += 1
                    return
            # Если лимит достигнут, ждём 1 секунду и проверяем снова
            await asyncio.sleep(1)

    async def send_message(self, bot: "Bot", chat_id: int, text: str):
        """
        Гарантированно отправляет сообщение, ожидая освобождения лимитов.
        Блокирует выполнение до тех пор, пока сообщение не будет отправлено.
        """
        # print(f"Ожидание лимитов для пользователя {chat_id}...")

        # Сначала ждём возможности отправить по глобальному лимиту
        await self.wait_for_global_limit()

        # Затем ждём возможности отправить пользователю (не чаще 1 в секунду)
        await self.wait_for_user_limit(chat_id)

        try:
            # Отправляем сообщение
            await bot.send_message(chat_id=chat_id, text=text)
            # print(f"Сообщение успешно отправлено пользователю {chat_id}")
        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю {chat_id}: {e}")
            # При ошибке возвращаем использованное место в глобальном лимите
            async with self.total_messages_lock:
                self.total_messages_sent -= 1
            raise  # Передаём ошибку выше для обработки
