"""from keyboards.inline import *

class SubCheck(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        chat_member = await event.bot.get_chat_member(-1002363411386, event.from_user.id)
        if chat_member.status == "left":
            await event.answer("💠 Подпишись на канал чтобы продолжить работу в боте", reply_markup=sub_key())
        else:
            return await handler(event, data)"""

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Awaitable, Dict, Any
from cachetools import TTLCache


class AntiFlood(BaseMiddleware):
    def __init__(self, time_limit: int = 3) -> None:
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        if event.chat.id in self.limit:
            return
        else:
            self.limit[event.chat.id] = None
        return await handler(event, data)