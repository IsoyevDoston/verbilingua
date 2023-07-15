from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

Menu = InlineKeyboardMarkup(row_width=1)
Menu.add(
    InlineKeyboardButton(text="👥Gender", callback_data="gender"),
    InlineKeyboardButton(text="🌟Interests", callback_data="interests"),
    InlineKeyboardButton(text="📅Age group", callback_data="age_group"),
    InlineKeyboardButton(text="👑Buy premium", callback_data="premium_trigger")
)

genderMenu = InlineKeyboardMarkup(row_width=1)
genderMenu.add(
        InlineKeyboardButton(text="Man👨", callback_data="man"),
        InlineKeyboardButton(text="Woman👩", callback_data="woman"),
        InlineKeyboardButton(text="Back🔙", callback_data="back_menu")
)

interests = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="Travel", callback_data="travel"),
        InlineKeyboardButton(text="Sport", callback_data="sport")
    ],
    [
        InlineKeyboardButton(text="Pets", callback_data="pets"),
        InlineKeyboardButton(text="Anime", callback_data="anime")
    ],
    [
        InlineKeyboardButton(text="Game", callback_data="game"),
        InlineKeyboardButton(text="Meme", callback_data="meme")
    ],
    [
        InlineKeyboardButton(text="Book", callback_data="book"),
        InlineKeyboardButton(text="Movie", callback_data="movie")
    ],
    [
        InlineKeyboardButton(text="Business", callback_data="business"),
        InlineKeyboardButton(text="Science", callback_data="science")
    ],
    [
        InlineKeyboardButton(text="Back🔙", callback_data="back_menu")
    ]
])

age_group = InlineKeyboardMarkup(row_width=2)
age_group.add(
        InlineKeyboardButton(text="up to 14", callback_data="age_14"),
        InlineKeyboardButton(text="15 to 17", callback_data="age15_17"),
        InlineKeyboardButton(text="18 to 21", callback_data="age18_21"),
        InlineKeyboardButton(text="22 to 25", callback_data="age22_25"),
        InlineKeyboardButton(text="26 to 35", callback_data="age26_35"),
        InlineKeyboardButton(text="from 36", callback_data="age_36"),
        InlineKeyboardButton(text="Back🔙", callback_data="back_menu")
)

