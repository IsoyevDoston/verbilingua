import asyncio
import datetime
import pytz
from aiogram import types
import asyncpg

from loader import dp, bot, db
from src.data.config import CHANNELS, ADMINS
from src.handlers.users.Personaldata import start_registration
from src.utils.misc import subscription
from src.keyboards.default.menu import Mainmenu



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Check if the user is already in the registration process
    telegram_id = message.from_user.id
    current_state = await db.check_current_state(telegram_id)
    if current_state is not None:
        user_id = message.from_user.id
        channels_keyboard = types.InlineKeyboardMarkup(row_width=1)
        for index, channel in enumerate(CHANNELS):
            status = await subscription.check(user_id=user_id, channel=channel)
            if not status:
                channels_keyboard.add(types.InlineKeyboardButton(text=f"Channel #{index+1}", url=await bot.export_chat_invite_link(channel)))
        if channels_keyboard.inline_keyboard:
            channels_keyboard.add(types.InlineKeyboardButton(text="Done ✅", callback_data="check_subs"))
            await message.answer('😔 You haven\'t subscribed to our channels yet!\n\nSubscribe and click "Done ✅"', reply_markup=channels_keyboard, disable_web_page_preview=True)
        else:
            await message.answer("Welcome to the bot!", reply_markup=Mainmenu)

    else:
        user = None
        try:
            user = await db.add_user(full_name=message.from_user.full_name,
                                     username=message.from_user.username,
                                     telegram_id=message.from_user.id)
        except asyncpg.exceptions.UniqueViolationError:
            pass

        if user is None:
            user = await db.select_user(telegram_id=message.from_user.id)

        count = await db.count_users()
        msg = f"{user[1]}:@{user[2]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)

        # User is already in the registration process
        await start_registration(message)  # Resend the registration inline keyboard

        # inviter_id = get_inviter_id_from_start_command(message.text)
        # if inviter_id is not None and inviter_id == telegram_id:  # Check if the inviter ID is the same as the user's ID
        #     # Check if the inviter has premium status
        #     premium_expiration = await db.get_user_premium_expiration(inviter_id)
        #     current_time = datetime.datetime.now(pytz.utc)
        #     if premium_expiration and premium_expiration > current_time:
        #         remaining_time = premium_expiration - current_time
        #         await message.answer(
        #             f"You were referred by an existing user.\nYou already have premium status.\nRemaining time: {remaining_time}")
        #     else:
        #         # Grant premium status to the inviter and the new user
        #         expiration_time = current_time + datetime.timedelta(minutes=30)
        #         await db.update_user_premium_expiration(inviter_id, expiration_time)
        #         await db.update_user_premium_status(inviter_id, True)  # Update the inviter's status to True (premium user)
        #
        #         await db.update_user_premium_expiration(telegram_id, expiration_time)
        #         await db.update_user_premium_status(telegram_id, True)  # Update the new user's status to True (premium user)
        #
        #         await message.answer(
        #             "You were referred by an existing user.\nCongratulations! You and the new user have been granted a 30-minute premium status.")
        # elif inviter_id is not None:
        #     await message.answer("You need to invite a new user to get the premium status.")
        # else:
        #     await message.answer("Welcome to the bot!", reply_markup=Mainmenu)

"This is get inviter id for affiliate marketing purposes"
# def get_inviter_id_from_start_command(command_text):
#     if command_text is not None and command_text.startswith('/start'):
#         referral_param = command_text.split()[1]
#         if referral_param.startswith('https://t.me/verbilingua_bot?start='):
#             # Extract the inviter ID from the referral parameter
#             inviter_id = referral_param.split('=')[1]
#             # Check if the inviter ID is a valid integer
#             if inviter_id.isdigit():
#                 return int(inviter_id)
#     return None

"it is for affiliate marketing, Right now it is not working well"
# async def check_premium_status():
#     while True:
#         users = await db.select_all_users()
#         current_time = datetime.datetime.now(pytz.utc)
#
#         for user in users:
#             user_id = user['telegram_id']
#             premium_expiration = user['premium_expiration']
#             status = user['status']
#
#             if status and premium_expiration <= current_time:
#                 await db.update_user_premium_status(user_id, False)  # Update status to False
#         await asyncio.sleep(60)  # Check every 60 seconds


"Deeplink start for ads"
# Template https://t.me/BOT_ID?start=specific_key
# @dp.message_handler(CommandStart(deep_link='example'))
# async def bot_start(message: types.Message):
#     user_id = message.from_user.id
#     channels_keyboard = types.InlineKeyboardMarkup(row_width=1)
#     for i, channel in enumerate(CHANNELS):
#         status = await subscription.check(user_id=user_id, channel=channel)
#         if not status:
#             channels_keyboard.add(
#                 types.InlineKeyboardButton(text=f"Channel #{i + 1}", url=await bot.export_chat_invite_link(channel)))
#     if channels_keyboard.inline_keyboard:
#         channels_keyboard.add(types.InlineKeyboardButton(text="Done ✅", callback_data="check_subs"))
#         await message.answer('😔 You haven\'t subscribed to our channels yet!\nSubscribe and click "Done ✅"!"',
#                              reply_markup=channels_keyboard, disable_web_page_preview=True)
#     else:
#         await message.answer("Welcome to the bot!", reply_markup=Mainmenu)
#     user = None
#     try:
#         user = await db.add_user(full_name=message.from_user.full_name,
#                                  username=message.from_user.username,
#                                  telegram_id=message.from_user.id)
        # Start the registration process by calling the registration handler
        # await start_registration(message)  # Fix: Pass 'message' instead of 'callback_query.message'
    # except asyncpg.exceptions.UniqueViolationError:
    #     pass
    #
    # if user is None:
    #     user = await db.select_user(telegram_id=message.from_user.id)












