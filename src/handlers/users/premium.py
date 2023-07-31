import pytz
import requests
import datetime

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import dp, bot, db
from aiogram import types

@dp.message_handler(text='💎Vip search')
@dp.message_handler(commands=['premium'])
async def premium_handler(message: types.Message):
    # Check the user's premium status
    telegram_id = message.from_user.id
    premium_status = await db.get_user_premium_status(telegram_id)

    if premium_status:
        # User has premium status
        # Show the premium menu with default keyboards
        premium_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        premium_keyboard.add(
                    KeyboardButton(text="Search 🙍‍♀️", callback_data="woman_search"),
                    KeyboardButton(text="Search 🙍‍♂️", callback_data="man_search"),
                    KeyboardButton(text="Random 👫", callback_data="vip_search"),
        )
        await message.reply("Welcome to the premium menu!", reply_markup=premium_keyboard)
    else:
        # User doesn't have premium status
        image_url = "https://i.ibb.co/FVKvp7X/vippic.jpg"
        response = requests.get(image_url)
        response.raise_for_status()
        # Get the image content
        image_content = response.content
        caption = """
By purchasing a subscription, you can enjoy the following benefits:

📌 Top priority in search 🔥

📌 Gender-specific search
👩 Premium subscribers can exclusively search for girls or boys

📌 Access to detailed interlocutor information
📂 Premium subscribers can view the gender, interests, and age of their conversation partner

📌 Ad-free experience
📲 We do not display any advertisements to our premium subscribers

📌 Dedicated chat support
🎁 Your support enables us to introduce new features, enhance chat moderation, and invest in advertising to attract more interlocutors.
"""

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton(text="🔥 1 week - $1.49 / 15ming so'm", url="https://t.me/verbilingua_admin"),
            types.InlineKeyboardButton(text="1 month - $2.99 / 30ming so'm", url="https://t.me/verbilingua_admin"),
            types.InlineKeyboardButton(text="1 year - $11.99 / 120ming so'm", url="https://t.me/verbilingua_admin"),
            # types.InlineKeyboardButton("Free VIP subscription", callback_data="free_premium_subscription"),
        )


        await message.answer_photo(
            photo=image_content,
            caption=caption,
            reply_markup=keyboard
        )

def get_inviter_id_from_start_command(command_text):
    if command_text is not None and command_text.startswith('/start'):
        referral_param = command_text.split()[1]
        if referral_param.startswith('https://t.me/verbilingua_bot?start='):
            # Extract the inviter ID from the referral parameter
            inviter_id = referral_param.split('=')[1]
            # Check if the inviter ID is a valid integer
            if inviter_id.isdigit():
                return int(inviter_id)
    return None


@dp.callback_query_handler(text="free_premium_subscription")
async def free_vip_handler(query: types.CallbackQuery):
    inviter_id = query.from_user.id
    affiliate_link = f"https://t.me/verbilingua_bot?start={inviter_id}"

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("Forward to Someone", callback_data="forward_message")
    )

    invited_users = await db.get_invited_users_count(inviter_id)
    premium_expiration = await db.get_user_premium_expiration(inviter_id)

    current_time = datetime.datetime.now(pytz.utc)
    if premium_expiration and premium_expiration > current_time:
        remaining_time = premium_expiration - current_time
        await query.message.answer(f"You already have premium status.\nRemaining time: {remaining_time}")
    else:
        # Check if the user entered through a referral link
        inviter_id_from_start = get_inviter_id_from_start_command(query.message.text)
        if inviter_id_from_start and inviter_id_from_start == inviter_id:
            # Grant premium status for 30 minutes to the inviter and the new user
            expiration_time = current_time + datetime.timedelta(minutes=30)
            await db.update_user_premium_expiration(inviter_id, expiration_time)
            await db.update_user_invited_users(inviter_id)  # Increment the inviter's invited_users count

            await db.update_user_premium_expiration(inviter_id_from_start, expiration_time)
            await db.update_user_premium_status(inviter_id_from_start, True)  # Update the invited user's premium status

            await query.message.answer("Congratulations! You and the new user have been granted a 30-minute premium status.")
        else:
            await query.message.answer("You need to invite a new user to get the premium status.")

    # Update the inviter's premium status after the 30-minute period
    inviter_premium_expiration = await db.get_user_premium_expiration(inviter_id)
    if inviter_premium_expiration and inviter_premium_expiration <= current_time:
        await db.update_user_premium_status(inviter_id, False)

    caption = f"Invite users using your link and get 👑VIP status for 30 minutes for each!\n\nInvited: {invited_users + 1}\n\nYour personal link:\n👉 {affiliate_link}"
    await query.message.edit_caption(caption=caption, reply_markup=keyboard)


@dp.callback_query_handler(text="forward_message")
async def forward_message_handler(query: types.CallbackQuery):
    inviter_id = query.from_user.id
    affiliate_link = f"https://t.me/verbilingua_bot?start={inviter_id}"
    invited_users = await db.get_invited_users_count(inviter_id)

    text_to_forward = f"Bot for language learning in Telegram! 🎭\n" \
                      "Search by gender, interests, and age 🌍\n\n" \
                      "Register using my link to get VIP status! 🌟\n\n" \
                      f"👉 [Join Now]({affiliate_link}) 👈"

    current_time = datetime.datetime.now(pytz.utc)
    # Grant the inviter a 30-minute premium status
    expiration_time = current_time + datetime.timedelta(minutes=30)
    await db.update_user_premium_expiration(inviter_id, expiration_time)
    await db.update_user_invited_users(inviter_id)  # Increment the inviter's invited_users count

    # Forward the message to another user
    await bot.forward_message(chat_id=query.from_user.id, from_chat_id=query.message.chat.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text=text_to_forward, parse_mode='Markdown')

    caption = f"Invite users using your link and get 👑VIP status for 30 minutes for each!\n\nInvited: {invited_users + 1}\n\nYour personal link:\n👉 {affiliate_link}"
    await query.message.edit_caption(caption=caption)





