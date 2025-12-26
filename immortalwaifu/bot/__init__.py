# ------------------------------ IMPORTS ---------------------------------
import logging
import os
import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client, filters

# Load environment variables from .env file
load_dotenv()

# --------------------------- LOGGING SETUP ------------------------------
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

# ---------------------------- CONSTANTS ---------------------------------
api_id = os.getenv("API_ID", "30999105")
api_hash = os.getenv("API_HASH", "b1d3a4e0b8c48ca9b1fad5f86eaa786b")
TOKEN = os.getenv("TOKEN", "8462520067:AAH8yXrfrDhbRJhARR2fslbTL2oh-9lTqDQ")
GLOG = os.getenv("GLOG", "-1002890863384")
CHARA_CHANNEL_ID = os.getenv("CHARA_CHANNEL_ID", "-1002890863384")
SUPPORT_CHAT_ID = os.getenv("SUPPORT_CHAT_ID", "-1002839513619")
mongo_url = os.getenv(
    "MONGO_URL",
    "mongodb+srv://Immortal_X_Xwaifu:SagarGupta0902@waifu.bebbu8f.mongodb.net/waifu?retryWrites=true&w=majority&appName=waifu"
)

# Modified to support both image and video URLs
START_MEDIA = os.getenv(
    "START_MEDIA",
    "https://files.catbox.moe/7ccoub.jpg,https://telegra.ph/file/1a3c152717eb9d2e94dc2.mp4"
).split(',')

PHOTO_URL = [
    os.getenv("PHOTO_URL_1", "https://files.catbox.moe/7ccoub.jpg"),
    os.getenv("PHOTO_URL_2", "https://files.catbox.moe/7ccoub.jpg")
]

SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/+eg1W0oek5CMwYzg1")
UPDATE_CHAT = os.getenv("UPDATE_CHAT", "https://t.me/+eg1W0oek5CMwYzg1")
SUDO = list(map(int, os.getenv("SUDO", "7765919932,7939978991").split(',')))
OWNER_ID = int(os.getenv("OWNER_ID", "7765919932"))

# --------------------- TELEGRAM BOT CONFIGURATION -----------------------
# ✅ FIXED: `f` hata diya, direct filters use kiya
command_filter = filters.create(lambda _, __, message: message.text and message.text.startswith("/"))

# Agar aap Application use nahi kar rahe to ye hata do, warna python-telegram-bot install karo
try:
    from telegram.ext import Application
    application = Application.builder().token(TOKEN).build()
except ImportError:
    application = None  # Render me agar python-telegram-bot nahi hai to crash nahi hoga

ZYRO = Client("Shivu", api_id=api_id, api_hash=api_hash, bot_token=TOKEN)

# -------------------------- DATABASE SETUP ------------------------------
try:
    ddw = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
    db = ddw['hinata_waifu']
    # Test the connection
    ddw.admin.command('ping')
    print("✅ Database connected successfully")
except Exception as e:
    print(f"⚠️ Database connection error: {e}")
    ddw = None
    db = None

# Collections
if db is not None:
    user_totals_collection = db['gaming_totals']
    group_user_totals_collection = db['gaming_group_total']
    top_global_groups_collection = db['gaming_global_groups']
    pm_users = db['gaming_pm_users']
    destination_collection = db['gamimg_user_collection']
    destination_char = db['gaming_anime_characters']
else:
    # Create mock collections if database connection failed
    user_totals_collection = None
    group_user_totals_collection = None
    top_global_groups_collection = None
    pm_users = None
    destination_collection = None
    destination_char = None

# -------------------------- GLOBAL VARIABLES ----------------------------
app = ZYRO
sudo_users = SUDO
collection = destination_char
user_collection = destination_collection

locks = {}
message_counters = {}
spam_counters = {}
last_characters = {}
sent_characters = {}
first_correct_guesses = {}
message_counts = {}
last_user = {}
warned_users = {}
user_cooldowns = {}
user_nguess_progress = {}
user_guess_progress = {}
normal_message_counts = {}

# -------------------------- POWER SETUP --------------------------------
from .unit.zyro_ban import *
from .unit.zyro_sudo import *
from .unit.zyro_react import *
from .unit.zyro_log import *
from .unit.zyro_send_img import *
from .unit.zyro_rarity import *
# ------------------------------------------------------------------------

async def PLOG(text: str):
    try:
        await app.send_message(
            chat_id=GLOG,
            text=text
        )
    except Exception as e:
        print(f"⚠️ Logging error: {e}")
