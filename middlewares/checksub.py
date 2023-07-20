from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from src.data.config import CHANNELS
from src.utils.misc import subscription

from loader import bot, dp, db


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            telegram_id = update.message.from_user.id
            current_state = await db.check_current_state(telegram_id)
            if current_state is not None:
                user = update.message.from_user.id
                if update.message.text in ['/start', '/help']:
                    return

                channels_keyboard = types.InlineKeyboardMarkup(row_width=1)
                for i, channel in enumerate(CHANNELS):
                    status = await subscription.check(user_id=user, channel=channel)
                    if not status:
                        channels_keyboard.add(types.InlineKeyboardButton(text=f"Channel #{i + 1}",
                                                                         url=await bot.export_chat_invite_link(channel)))

                if channels_keyboard.inline_keyboard:
                    channels_keyboard.add(types.InlineKeyboardButton(text="Done ✅", callback_data="check_subs"))
                    await update.message.answer('😔 You haven\'t subscribed to our channels yet!\n\nSubscribe and click "Done ✅"', reply_markup=channels_keyboard, disable_web_page_preview=True)

        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data == "check_subs":
                final_status = True
                for channel in CHANNELS:
                    status = await subscription.check(user_id=user, channel=channel)
                    final_status *= status
                if final_status:
                    await bot.answer_callback_query(update.callback_query.id, text="You have subscribed to all the required channels!")
                    await bot.delete_message(update.callback_query.message.chat.id, update.callback_query.message.message_id)
                else:
                    await bot.answer_callback_query(update.callback_query.id, text="Please subscribe to all the required channels before using the bot.")



