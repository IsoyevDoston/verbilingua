import os
from aiogram import types
import pandas as pd
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import filters
from loader import dp, db, bot

from src.data.config import *

@dp.message_handler(chat_id=ADMINS, commands=['admin'])
async def show_admin_commands(message: types.Message):
    text = ("Handlers for admins on @verbilingua_bot\n",
            "/data - export all data in the bot",
            "/ids - export all telegram id inside the bot",
            "/find_user - find user through telegram id",
            "/add_channel - add mandatory channel (You must give admin in this channel of bot before)",
            "/remove_channel  - remove mandatory channel",
            "/update_status - update user status to premium",
            "/drop_status - drop user status to normal\n"
            "/statistics - show all statistics in the bot",
            "/post - post for all users",
            "/w_post - post for female's ads",
            "/m_post post for male's ads")

    await message.answer("\n".join(text))
def format_user_data(users):
    # Create a DataFrame from the user data
    df = pd.DataFrame(users)

    # Rename the columns
    df = df.rename(columns={
        'id': 'ID',
        'full_name': 'Full Name',
        'username': 'Username',
        'telegram_id': 'Telegram ID',
        'gender': 'Gender',
        'interests': 'Interests',
        'age_group': 'Age Group',
        'status': 'Status',
        'state_registration': 'Registration State',
        'invited_users': 'Invited Users',
        'premium_expiration': 'Premium Expiration',
        'created_at': 'Created At'
    })

    return df

@dp.message_handler(chat_id=ADMINS, commands=['data'])
async def export_user_data(message: types.Message):
    # Retrieve all the user data from the database
    users = await db.select_all_users()

    # Format the user data as a DataFrame
    df = format_user_data(users)

    # Export the DataFrame as a CSV file
    csv_file = 'user_data.csv'
    df.to_csv(csv_file, index=False)

    await bot.send_document(chat_id=message.chat.id, document=open(csv_file, 'rb'), caption='User Data CSV')

    # Remove the temporary file
    os.remove(csv_file)

@dp.message_handler(chat_id=ADMINS, commands=["ids"])
async def all_ids_command(message: types.Message):
    # Retrieve all user IDs from the Users table
    result = await db.select_all_ids()

    if result is None:
        await message.answer("No Telegram IDs found.")
        return

    # Extract the Telegram IDs from the query result
    telegram_ids = [row["telegram_id"] for row in result]

    # Format the Telegram IDs as a string
    telegram_ids_str = "\n".join(str(telegram_id) for telegram_id in telegram_ids)

    await message.answer(f"Telegram IDs:\n{telegram_ids_str}")


@dp.message_handler(chat_id=ADMINS, commands=['find_user'])
async def find_user_data(message: types.Message):
    # Get the Telegram ID from the command arguments
    try:
        telegram_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.reply("Please provide a valid Telegram ID.")
        return

    # Retrieve user data based on the Telegram ID
    user_data = await db.select_user_telegram_id(telegram_id)

    # Check if the user exists
    if not user_data:
        await message.reply("User not found.")
        return

    # Format and send the user data as a message
    user_info = f"👤About user (@{user_data['username']}) - {user_data['telegram_id']}\n\n"
    user_info += f" ID : {user_data['id']}\n"
    user_info += f" Full Name: {user_data['full_name']}\n"
    user_info += f" Username : {user_data['username']}\n"
    user_info += f" Telegram ID : {user_data['telegram_id']}\n"
    user_info += f" Gender : {user_data['gender']}\n"
    user_info += f" Interests : {user_data['interests']}\n"
    user_info += f" Age Group : {user_data['age_group']}\n"
    user_info += f" Status : {user_data['status']}\n"
    user_info += f" State of registration : {user_data['current_state']}\n"
    user_info += f" Invited Users : {user_data['invited_users']}\n"
    user_info += f" Premium Expiration': {user_data['premium_expiration']}\n"
    user_info += f" User Created at : {user_data['created_at']}"

    await message.answer(user_info)


@dp.message_handler(chat_id=ADMINS, commands=['add_channel'])
async def add_channel(message: types.Message):
    new_channel = message.get_args()
    CHANNELS.append(new_channel)
    if new_channel in CHANNELS:
        await message.reply(f"The channel {new_channel} has been added.\n(Note: Please make sure bot need to be admin in this channel  ")
    else:
        await message.reply(f"The {new_channel} was not added.\n(Note: Please make sure bot need to be admin in this channel   ")


@dp.message_handler(chat_id=ADMINS, commands=['remove_channel'])
async def remove_channel(message: types.Message):
    channel_to_remove = message.get_args()
    if channel_to_remove in CHANNELS:
        CHANNELS.remove(channel_to_remove)
        await message.reply(f"The channel {channel_to_remove} has been removed.")
    else:
        await message.reply(f"The channel {channel_to_remove} was not found.")

@dp.message_handler(chat_id=ADMINS, commands=['update_status'])
async def update_user_status(message: types.Message):
    # Extract the telegram_id from the command message
    try:
        telegram_id = int(message.get_args())
    except ValueError:
        await message.reply("Invalid user ID. Please provide a valid user ID.")
        return

    # Check if the user exists in the database
    user = telegram_id
    if user:
        # Update the user's premium status to True
        await db.update_user_premium_status(telegram_id, True)

        # Check if the user's premium status was successfully updated
        premium_status = await db.get_user_premium_status(telegram_id)
        if premium_status:
            await message.reply("User added to premium status successfully.")
        else:
            await message.reply("Failed to update user's premium status.")
    else:
        await message.reply("User not found in the database.")

@dp.message_handler(chat_id=ADMINS, commands=['drop_status'])
async def drop_user_status(message: types.Message):
    # Extract the telegram_id from the command message
    try:
        telegram_id = int(message.get_args())
    except ValueError:
        await message.reply("Invalid user ID. Please provide a valid user ID.")
        return

    # Check if the user exists in the database
    user = telegram_id
    if user:
        # Update the user's premium status to False
        await db.update_user_premium_status(telegram_id, False)

        # Check if the user's premium status was successfully updated
        premium_status = await db.get_user_premium_status(telegram_id)
        if not premium_status:
            await message.reply("User removed from premium status successfully.")
        else:
            await message.reply("Failed to update user's premium status.")
    else:
        await message.reply("User not found in the database.")



@dp.message_handler(chat_id=ADMINS, commands=['statistics'])
async def show_data(message: types.Message):
    # Count all users
    total_users = await db.count_users()
    # Count men and women
    total_men = await db.count_men()
    total_women = await db.count_women()
    # Count new users within the last 24 hours
    new_users = await db.count_new_users()

    statistics_message = [
        f"👥 Total users: {total_users}",
        f"👨 Total male users: {total_men}",
        f"👩 Total female users:  {total_women}",
        f"⏳ New users in the last 24 hours: {new_users}\n"
        "📊 Statistics for @verbilingua_bot",
    ]
    await message.answer('\n'.join(statistics_message))

class MyState(StatesGroup):
    waiting_for_post = State()
    waiting_for_female_post = State()
    waiting_for_male_post = State()


@dp.message_handler(filters.Command(commands=['post']), chat_id=ADMINS)
async def send_to_all_start(message: types.Message):
    # Start a conversation with the admin
    await message.answer("Send me your post. You can include images, captions, inline keyboards, and links.")

    # Set the state to wait for the post content
    await MyState.waiting_for_post.set()

@dp.message_handler(state=MyState.waiting_for_post, content_types=types.ContentType.ANY)
async def send_to_all_post(message: types.Message, state: FSMContext):
    # Retrieve all users from the database
    users = await db.select_all_users()

    # Iterate over all users and forward a copy of the original message individually
    for user in users:
        # Create a copy of the original message
        try:
            new_message = await bot.copy_message(chat_id=user['telegram_id'], from_chat_id=message.chat.id, message_id=message.message_id)
        except Exception as e:
            # Handle any exceptions that occur during message forwarding
            await message.reply(f"Failed to forward message to user {user['telegram_id']}: {str(e)}")

    # Reset the state to the initial state
    await state.finish()

    # Notify the admin about the successful forwarding of the post
    await message.answer(f"Post sent to {len(users)} users!")


@dp.message_handler(chat_id=ADMINS, commands=['w_post'])
async def send_to_all_females(message: types.Message):
    # Retrieve all female users from the database
    await message.answer("Send me your female's post. You can include images, captions, inline keyboards, and links.")
    # Set the state to wait for the post content for female users
    await MyState.waiting_for_female_post.set()

@dp.message_handler(state=MyState.waiting_for_female_post, content_types=types.ContentType.ANY)
async def send_to_all_female_post(message: types.Message, state: FSMContext):

    female_users = await db.get_female_users()
    await forward_post_to_users(female_users, message)

    # Reset the state to the initial state
    await state.finish()

    # Notify the admin about the successful forwarding of the post
    await message.answer(f"Post sent to {len(female_users)} female users!")


@dp.message_handler(chat_id=ADMINS, commands=['m_post'])
async def send_to_all_males(message: types.Message):
    # Retrieve all male users from the database
    await message.answer("Send me your male's post. You can include images, captions, inline keyboards, and links.")
    # Set the state to wait for the post content for male users
    await MyState.waiting_for_male_post.set()

@dp.message_handler(state=MyState.waiting_for_male_post, content_types=types.ContentType.ANY)
async def send_to_all_male_post(message: types.Message, state: FSMContext):

    male_users = await db.get_male_users()
    await forward_post_to_users(male_users, message)

    # Reset the state to the initial state
    await state.finish()

    # Notify the admin about the successful forwarding of the post
    await message.answer(f"Post sent to {len(male_users)} male users!")

async def forward_post_to_users(users, message):
    # Iterate over all users and forward the post individually
    for user in users:
        try:
            await bot.copy_message(chat_id=user['telegram_id'], from_chat_id=message.chat.id, message_id=message.message_id)
        except Exception as e:
            # Handle any exceptions that occur during message forwarding
            await message.reply(f"Failed to forward message to user {user['telegram_id']}: {str(e)}")




















