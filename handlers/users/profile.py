from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from src.handlers.users.premium import premium_handler
from src.keyboards.inline.profile_keyboards import *
from loader import dp, db, bot


@dp.message_handler(text='👤Profile')
@dp.message_handler(commands=["profile"])
async def select_category(message: Message):
    telegram_id = message.from_user.id

    gender = await db.get_user_gender(telegram_id)
    interests = await db.get_user_interests(telegram_id)
    age_group = await db.get_user_age_group(telegram_id)
    premium = await db.get_user_premium_status(telegram_id)

    if gender:
        profile_message = f"👥 Gender - {gender}\n"
    else:
        profile_message = f"👥 Gender - None specified\n"
    if interests:
        profile_message += f"🌟 Interests - {interests}\n"
    else:
        profile_message += f"🌟 Interests - Not specified\n"
    profile_message += f"📅 Age - {age_group}\n"
    if premium == "true":
        profile_message += f"💎 Vip status - Premium user\n"
    else:
        profile_message += f"💎 Vip status - None\n"
    profile_message += "\nPlease select the settings you wish to modify:"

    # Send the profile message to the user
    await message.answer(profile_message, reply_markup=Menu)

@dp.callback_query_handler(text_contains="premium_trigger")
async def handle_callback(call: CallbackQuery):
    if call.data == "premium_trigger":
        await premium_handler(call.message)
        await call.message.delete()
        await call.answer(cache_time=60)

@dp.callback_query_handler(text_contains="gender")
async def choose_gender(call: CallbackQuery):
    await call.message.answer("Please select your gender:", reply_markup=genderMenu)
    await call.message.delete()
    await call.answer(cache_time=60)

@dp.callback_query_handler(lambda c: c.data in ['man','woman'])
async def process_gender_callback(call: CallbackQuery):
    gender = call.data
    telegram_id = call.from_user.id
    await db.update_user_gender(gender, telegram_id)
    await call.answer(f"Thank you for indicating your gender!")
    await call.answer(cache_time=60)

@dp.callback_query_handler(lambda c: c.data == "back_menu")
async def process_back_gender_callback(call: CallbackQuery):
    telegram_id = call.from_user.id

    gender = await db.get_user_gender(telegram_id)
    interests = await db.get_user_interests(telegram_id)
    age_group = await db.get_user_age_group(telegram_id)
    premium = await db.get_user_premium_status(telegram_id)

    if gender:
        profile_message = f"👥 Gender - {gender}\n"
    else:
        profile_message = f"👥 Gender - None specified\n"
    if interests:
        profile_message += f"🌟 Interests - {interests}\n"
    else:
        profile_message += f"🌟 Interests - Not specified\n"
    profile_message += f"📅 Age - {age_group}\n"
    if premium == "true":
        profile_message += f"💎 Vip status - Premium user\n"
    else:
        profile_message += f"💎 Vip status - None\n"
    profile_message += "\nPlease select the settings you wish to modify:"

    await call.message.answer(profile_message, reply_markup=Menu)
    await call.message.delete()
    await call.answer(cache_time=60)


interests_callback = CallbackData("interests", "interests_list")

@dp.callback_query_handler(text_contains="interests")
async def choose_interests(call: CallbackQuery):
    await call.message.answer("Please select your interests (up to 3):", reply_markup=interests)
    await call.answer(cache_time=60)

@dp.callback_query_handler(lambda c: c.data in ['travel', 'sport', 'pets', 'anime', 'game', 'meme', 'book', 'movie', 'business', 'science'])
async def process_interests_callback(call: CallbackQuery):
    interest = call.data
    telegram_id = call.from_user.id
    await db.update_user_interests(interest, telegram_id)
    await call.answer("Interest selected!")
    await call.answer(f"Your interest is {interest}", reply_markup=ReplyKeyboardRemove())

# @dp.callback_query_handler(lambda c: c.data == "clear_all")
# async def clear_all_interests_callback(call: CallbackQuery):
#     telegram_id = call.from_user.id
#     await db.clear_user_interests(telegram_id)
#     await call.answer("All interests cleared!")
#     await call.answer(cache_time=60)

@dp.callback_query_handler(lambda c: c.data == "back_menu")
async def process_back_interests_callback(call: CallbackQuery):
    telegram_id = call.from_user.id

    gender = await db.get_user_gender(telegram_id)
    interests = await db.get_user_interests(telegram_id)
    age_group = await db.get_user_age_group(telegram_id)
    premium = await db.get_user_premium_status(telegram_id)

    if gender:
        profile_message = f"👥 Gender - {gender}\n"
    else:
        profile_message = f"👥 Gender - None specified\n"
    if interests:
        profile_message += f"🌟 Interests - {interests}\n"
    else:
        profile_message += f"🌟 Interests - Not specified\n"
    profile_message += f"📅 Age - {age_group}\n"
    if premium == "true":
        profile_message += f"💎 Vip status - Premium user\n"
    else:
        profile_message += f"💎 Vip status - None\n"
    profile_message += "\nPlease select the settings you wish to modify:"

    await call.message.answer(profile_message, reply_markup=Menu)
    await call.message.delete()
    await call.answer(cache_time=60)

@dp.callback_query_handler(text_contains="age_group")
async def choose_age_group(call: CallbackQuery):
    await call.message.answer("Please select your age group:", reply_markup=age_group)
    await call.message.delete()
    await call.answer(cache_time=60)

@dp.callback_query_handler(lambda c: c.data in ['age_14', 'age15_17', 'age18_21', 'age22_25', 'age26_35', 'age_36'])
async def process_age_group_callback(call: CallbackQuery):
    age_group = call.data
    telegram_id = call.from_user.id
    await db.update_user_age_group(age_group, telegram_id)  # Update the user's age group in the database
    await call.answer(f"Thank you for indicating your age group!")
    await call.answer(cache_time=60)

@dp.callback_query_handler(lambda c: c.data == "back_menu")
async def process_back_age_group_callback(call: CallbackQuery):
    telegram_id = call.from_user.id

    gender = await db.get_user_gender(telegram_id)
    interests = await db.get_user_interests(telegram_id)
    age_group = await db.get_user_age_group(telegram_id)
    premium = await db.get_user_premium_status(telegram_id)

    if gender:
        profile_message = f"👥 Gender - {gender}\n"
    else:
        profile_message = f"👥 Gender - None specified\n"
    if interests:
        profile_message += f"🌟 Interests - {interests}\n"
    else:
        profile_message += f"🌟 Interests - Not specified\n"
    profile_message += f"📅 Age - {age_group}\n"
    if premium == "true":
        profile_message += f"💎 Vip status - Premium user\n"
    else:
        profile_message += f"💎 Vip status - None\n"
    profile_message += "\nPlease select the settings you wish to modify:"

    await call.message.answer(profile_message, reply_markup=Menu)
    await call.message.delete()
    await call.answer(cache_time=60)
