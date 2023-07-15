from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "🆕Restart bot"),
            types.BotCommand("search", "🔍Search partner"),
            types.BotCommand("stop", "🛑Stop conversation"),
            types.BotCommand("help", "🚨Bot help"),
            types.BotCommand("premium", "💎Become a VIP user"),
            types.BotCommand("link", "🔗Share a link to your Telegram profile"),
            types.BotCommand("profile", "⚙️Change your profile information"),
            types.BotCommand("rules", "👮Read the rules")
        ]
    )
