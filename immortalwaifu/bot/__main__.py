import asyncio
import importlib
from pyrogram import idle
from bot import *
from bot.modules import ALL_MODULES

def main():
    for module_name in ALL_MODULES:
        importlib.import_module(f"bot.modules.{module_name}")
    LOGGER("bot.modules").info("All Features Loaded Successfully ✅")

    asyncio.run(start_all())

async def start_all():
    ptb_started = False
    pyro_started = False

    try:
        # 🔹 Start Pyrogram
        if ZYRO:
            await ZYRO.start()
            pyro_started = True
            LOGGER("bot").info("Pyrogram started ✅")

        # 🔹 Start python-telegram-bot (NON blocking)
        if application:
            await application.initialize()
            await application.start()
            ptb_started = True
            LOGGER("bot").info("python-telegram-bot started ✅")

        LOGGER("bot").info("🤖 Bot is running...")
        idle()  # ⚠️ DO NOT await this

    except Exception as e:
        LOGGER("bot").error(f"Runtime error: {e}")

    finally:
        # 🔻 graceful shutdown (ONLY if started)
        if ptb_started:
            await application.stop()
            await application.shutdown()

        if pyro_started:
            await ZYRO.stop()

if __name__ == "__main__":
    main()
