from aiogram import types
from loader import dp, bot, db
from src.keyboards.default.menu import Mainmenu

@dp.message_handler(text="Search a friend🔎")
@dp.message_handler(commands=['search'])
async def search_command(message: types.Message):
    user_id = message.chat.id
    companion_id = await db.get_companion_id(user_id)
    premium_status = await db.get_user_premium_status(user_id)

    if companion_id is not None:
        user_gender = await db.get_user_gender(companion_id)  # Get companion's gender
        user_interests = await db.get_user_interests(companion_id)  # Get companion's interests
        user_age_group = await db.get_user_age_group(companion_id)  # Get companion's age group

        if premium_status or user_id == companion_id:
            await message.reply(f"Found someone for you! 🎯\n\n👫Gender: {user_gender}\n🌟Interests: {user_interests}\n📅Age: {user_age_group}\n\n/search - search for a new friend\n/stop - end the dialogue")
            await bot.send_message(companion_id, "Found someone for you! 🎯\n\n/search - search for a new friend\n/stop - end the dialogue")
        else:
            pass
    elif await db.is_in_conversation(user_id):
        await message.reply("You're already in the queue or dialogue 🤔\nSend /stop to stop the search or dialog.")
    else:
        companion_id = await db.get_available_companion_id(user_id)
        if companion_id is not None:
            await db.set_companion_id(user_id, companion_id)
            await db.set_companion_id(companion_id, user_id)
            user_gender = await db.get_user_gender(companion_id)
            user_interests = await db.get_user_interests(companion_id)
            user_age_group = await db.get_user_age_group(companion_id)

            if premium_status:
                await message.reply(f"Found someone for you! 🎯\n\n👫Gender: {user_gender}\n🌟Interests: {user_interests}\n📅Age: {user_age_group}\n\n/search - search for a new friend\n/stop - end the dialogue")
                await bot.send_message(companion_id, "Found someone for you! 🎯\n\n/search - search for a new friend\n/stop - end the dialogue")
            else:
                await message.reply("Found someone for you! 🎯\n\n/search - search for a new friend\n/stop - end the dialogue")
        else:
            await db.add_user_to_conversations(user_id)
            await message.reply("Looking for a friend...🔍")


@dp.message_handler(commands=['stop'])
async def stop_command(message: types.Message):
    user_id = message.chat.id
    if await db.is_in_conversation(user_id):
        companion_id = await db.get_companion_id(user_id)
        await db.remove_user_from_conversations(user_id)
        await db.remove_user_from_conversations(companion_id)
        await message.answer("You have ended the connection with your friend 🙄\n\nType /search to find the next one")
        await bot.send_message(companion_id, "Friend ended the connection with you 😞\n\nType /search to find the next one")
    else:
        await message.reply("You don't have a friend yet 😕\nType /search to start looking for one")


@dp.message_handler(content_types=["text", "sticker", "photo", "voice", "document"])
async def content_handler(message: types.Message):
    chat_info = await db.get_chat_info(message.chat.id)
    if chat_info is not None:
        user_id = chat_info["user_id"]
        companion_id = chat_info["companion_id"]
        recipient_id = companion_id if message.from_user.id == user_id else user_id

        if message.content_type == "sticker":
            await bot.send_sticker(chat_id=recipient_id, sticker=message.sticker.file_id)
        elif message.content_type == "photo":
            await bot.send_photo(chat_id=recipient_id, photo=message.photo[-1].file_id)
        elif message.content_type == "voice":
            await bot.send_voice(chat_id=recipient_id, voice=message.voice.file_id)
        elif message.content_type == "document":
            await bot.send_document(chat_id=recipient_id, document=message.document.file_id)
        else:
            await bot.send_message(chat_id=recipient_id, text=message.text)
















