import asyncio
import importlib
from bot import *
from bot.modules import ALL_MODULES

async def main():
    # load modules
    for module_name in ALL_MODULES:
        importlib.import_module(f"bot.modules.{module_name}")
    LOGGER("bot.modules").info("All Features Loaded Successfully ✅")

    # start pyrogram
    if ZYRO:
        await ZYRO.start()
        LOGGER("bot").info("Pyrogram started ✅")

    # start python-telegram-bot (non blocking)
    if application:
        await application.initialize()
        await application.start()
        LOGGER("bot").info("python-telegram-bot started ✅")

    LOGGER("bot").info("🤖 Bot is running (Render stable mode)")

    # 🔒 KEEP PROCESS ALIVE FOREVER
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
