from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Mainmenu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Search a friend🔎'),
        ],
        [
            KeyboardButton(text='💎Vip search')
        ],
        [
            KeyboardButton(text='💬 Chat room'),
            KeyboardButton(text='👤Profile'),
        ],
    ],
    resize_keyboard=True
)