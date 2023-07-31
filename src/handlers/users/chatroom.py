from aiogram import types
from loader import dp

from src.keyboards.default.menu import Mainmenu

@dp.message_handler(text="💬 Chat room")
async def chat_room(message: types.Message):
    invite_text = "Welcome to the Verbi Chat Room! 🎉\n\nJoin the conversation and connect with like-minded individuals on various topics. Share your thoughts, ask questions, and make new friends!\n\nClick the link below to join:\n\n[Verbi Chat Room](https://t.me/verbi_chatroom)"

    await message.answer(invite_text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=Mainmenu)