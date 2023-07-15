
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.builtin import Command
from loader import dp


@dp.message_handler(Command('rules'))
async def rules_handler(msg: types.Message):
    message = (
        "Please read the rules to learn which conversations are prohibited in the chat and how to get the most out of your language exchange experience. "
        "It's important to follow these guidelines to ensure a safe and respectful environment for all users.\n"
        "\nClick here to access the rules:\n"
        "https://telegra.ph/Rules-for-the-Verbi-bot-verbilingua-bot-04-19")
    await msg.answer(message)


async def delete_links(message: types.Message):
    if message.text:
        if "http" in message.text:
            await message.delete()

# Define a command handler for the /link command
@dp.message_handler(Command('link'))
async def link_command(message: types.Message):
    # Get the user's Telegram profile link
    user_link = f"https://t.me/{message.from_user.username}"
    # Send the link and partner's username to the conversation partner
    if user_link:
        await message.reply(f"<a href='{user_link}'>Click to go to a friends's telegram</a>")
    else:
        await message.reply(f"You have not set a username yet. Please set a username to use this feature.")


