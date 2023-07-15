import asyncio
from aiogram import types

from loader import dp

@dp.message_handler()
async def echo(message: types.Message):
    await asyncio.sleep(0.5)
    await message.answer(message.text)
