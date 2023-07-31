from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp

@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("This is a language exchange bot for English learners\n",
            "The bot can help you practice your English skills through anonymous conversations with other learners.\n",
            "Here are some useful commands:",
            "/start - restart bot",
            "/search - find a new conversation partner and start chatting",
            "/stop - end your conversation with your current partner whenever you want",
            "/premium - become a VIP user and unlock exclusive features",
            "/link - share a link to your Telegram profile with your conversation partner",
            "/profile - personalize your experience by changing your interests and other settings",
            "/rules - read the rules to ensure a safe and enjoyable chat experience")

    await message.answer("\n".join(text))
