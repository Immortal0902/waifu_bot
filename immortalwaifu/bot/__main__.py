import asyncio
import importlib
from bot import *
from bot.modules import ALL_MODULES
from pyrogram import idle

def main():
    for module_name in ALL_MODULES:
        importlib.import_module(f"bot.modules.{module_name}")
    LOGGER("bot.modules").info("All Features Loaded Successfully ✅")

    asyncio.run(start_all())

async def start_all():
    try:
        # 🔹 Start Pyrogram bot
        if ZYRO:
            await ZYRO.start()
            LOGGER("bot").info("Pyrogram started ✅")

        # 🔹 Start python-telegram-bot (NON-BLOCKING)
        if application:
            await application.initialize()
            await application.start()
            LOGGER("bot").info("python-telegram-bot started ✅")

        LOGGER("bot").info("🤖 Bot is running...")
        await idle()  # keeps event loop alive

    except Exception as e:
        LOGGER("bot").error(f"Runtime error: {e}")

    finally:
        # graceful shutdown (Render safe)
        if application:
            await application.stop()
            await application.shutdown()

        if ZYRO:
            await ZYRO.stop()

if __name__ == "__main__":
    main()
