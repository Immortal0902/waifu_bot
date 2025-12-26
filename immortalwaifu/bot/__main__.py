import os
import sys
import types
import importlib
import logging
from PIL import Image
import mimetypes

# ✅ Monkey-patch: Fake imghdr for python-telegram-bot (Python 3.13 Fix)
fake_imghdr = types.ModuleType("imghdr")

def detect_image_type(file_path: str):
    try:
        with Image.open(file_path) as img:
            return img.format.lower()  # Example: 'jpeg', 'png', 'webp'
    except:
        mime, _ = mimetypes.guess_type(file_path)
        return mime.split('/')[-1] if mime else None

fake_imghdr.what = detect_image_type
sys.modules["imghdr"] = fake_imghdr

# ✅ Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("telegram").setLevel(logging.ERROR)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

# ✅ Ensure correct package path when running directly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))

# ✅ Import Bot Modules
from bot import *
from bot.modules import ALL_MODULES

def main() -> None:
    # Import all custom modules
    for module_name in ALL_MODULES:
        importlib.import_module(f"bot.modules.{module_name}")
    LOGGER("bot.modules").info("All Features Loaded Successfully ✅")

    try:
        ZYRO.start()
        LOGGER("bot").info(
            "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY TEAMZYRO☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
        )
        
        # Send start message in a non-blocking way if needed, but skip for Render deployment
        # to avoid issues with hardcoded CHAT_ID in zyro_log.py
        # send_start_message() 
        
        # Start the bot based on available framework
        if application:
            # Run python-telegram-bot polling (this blocks)
            application.run_polling(drop_pending_updates=True)
        else:
            # Use Pyrogram's idle to keep the bot running (this blocks)
            from pyrogram import idle
            idle()
    except KeyboardInterrupt:
        LOGGER("bot").info("Bot stopped by user")
    except Exception as e:
        LOGGER("bot").error(f"Error while starting bot: {e}")

if __name__ == "__main__":
    main()
