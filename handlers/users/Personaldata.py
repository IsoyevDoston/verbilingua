from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot, db, dp
from src.states.PersonaldataState import PersonalData
from src.keyboards.default.menu import Mainmenu

class RegistrationMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_pre_process(self, message: types.Message, data: dict):
        # Check the current state of the user
        current_state = await db.check_current_state(message.from_user.id)
        if current_state is None:
            # User is not registered, continue with the registration flow
            await start_registration(message)
        else:
             # User is already registered, skip the registration flow
            pass

    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Check if the message is to start the registration process
        if message.text == "start_registration":
            # Start the registration process by calling the start_registration handler
            await start_registration(message)

# Register the middleware
dp.middleware.setup(RegistrationMiddleware())


# Define the registration handler
async def start_registration(message: types.Message):
    # Create an inline keyboard markup for the gender selection
    gender_keyboard = InlineKeyboardMarkup(row_width=2)
    gender_keyboard.add(
        InlineKeyboardButton(text="Men", callback_data="man"),
        InlineKeyboardButton(text="Woman", callback_data="woman")
    )

    # Send the gender selection message
    await message.answer("👣 Step 1 of 3\nChoose below what gender you are:", reply_markup=gender_keyboard)
    # Set the state to 'gender' to keep track of the registration step
    await PersonalData.gender.set()


# Define the gender selection callback handler
@dp.callback_query_handler(lambda c: c.data in ['man', 'woman'], state=PersonalData.gender)
async def answer_gender(callback_query: types.CallbackQuery, state: FSMContext):
    # Get the gender from the callback data
    gender = callback_query.data

    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    # Create an inline keyboard markup for the interest selection
    interest_keyboard = InlineKeyboardMarkup(row_width=2)
    interest_keyboard.add(
        InlineKeyboardButton(text="Travel", callback_data="travel"),
        InlineKeyboardButton(text="Sport", callback_data="sport"),
        InlineKeyboardButton(text="Pets", callback_data="pets"),
        InlineKeyboardButton(text="Anime", callback_data="anime"),
        InlineKeyboardButton(text="Game", callback_data="game"),
        InlineKeyboardButton(text="Meme", callback_data="meme"),
        InlineKeyboardButton(text="Book", callback_data="book"),
        InlineKeyboardButton(text="Movie", callback_data="movie"),
        InlineKeyboardButton(text="Business", callback_data="business"),
        InlineKeyboardButton(text="Science", callback_data="science")
    )

    # Update the user's gender in the state
    await state.update_data(gender=gender)

    # Send the interest selection message
    await bot.send_message(callback_query.from_user.id, "👣 Step 2 of 3\nSelect your interest:",
                           reply_markup=interest_keyboard)

    # Set the state to step2 to keep track of the registration step
    await PersonalData.interests.set()


# Define the interest selection callback handler
@dp.callback_query_handler(lambda c: c.data in ['travel', 'sport', 'pets', 'anime', 'game', 'meme', 'book', 'movie', 'business', 'science'], state=PersonalData.interests)
async def answer_interest(callback_query: types.CallbackQuery, state: FSMContext):
    # Get the interests from the callback data
    interests = callback_query.data

    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    # Create an inline keyboard markup for the age group selection
    age_group_keyboard = InlineKeyboardMarkup(row_width=2)
    age_group_keyboard.add(
        InlineKeyboardButton(text="up to 14", callback_data="age_14"),
        InlineKeyboardButton(text="15 to 17", callback_data="age_17"),
        InlineKeyboardButton(text="18 to 21", callback_data="age_21"),
        InlineKeyboardButton(text="22 to 25", callback_data="age_25"),
        InlineKeyboardButton(text="26 to 35", callback_data="age_35"),
        InlineKeyboardButton(text="from 36", callback_data="age_36")
    )

    # Update the user's interests in the state
    await state.update_data(interests=interests)

    # Send the age group selection message
    await bot.send_message(callback_query.from_user.id, "👣 Step 3 of 3\nSelect your age group:",
                           reply_markup=age_group_keyboard)

    # Set the state to step3 to keep track of the registration step
    await PersonalData.age.set()


# Define the age group selection callback handler
@dp.callback_query_handler(lambda c: c.data in ['age_14', 'age_17', 'age_21', 'age_25', 'age_35', 'age_36'], state=PersonalData.age)
async def answer_age_group(callback_query: types.CallbackQuery, state: FSMContext):
    # Get the age group from the callback data
    age_group = callback_query.data

    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    telegram_id = callback_query.from_user.id
    # Update the user's age group in the state
    await state.update_data(age_group=age_group)
    data = await state.get_data()
    gender = data.get('gender')
    interests = data.get('interests')
    # Store the user's registration data in the database
    await db.update_user_age_group(age_group, telegram_id)
    await db.update_user_gender(gender, telegram_id)
    await db.update_user_interests(interests, telegram_id)

    current_state = "checked"  # Set the current state to "checked" or any other appropriate value
    # Update the user's current state in the database
    await db.update_user_current_state(telegram_id, current_state)

    # Send the final message
    await bot.send_message(callback_query.from_user.id, "✅ Registration completed successfully!", reply_markup=Mainmenu)

    # End the state and return to the initial state
    await state.finish()


