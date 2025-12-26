import os
import importlib.util
import random
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import ChatWriteForbidden
from bot import *
from bot.unit.zyro_help import HELP_DATA

# 🔹 Function to Calculate Uptime
START_TIME = time.time()

def get_uptime():
    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# 👑 Owner Username (WITHOUT @)
OWNER_USERNAME = "immortal_in_world"  # Bas username likho, @ mat lagao

# 🔹 Function to Generate Private Start Message & Buttons
async def generate_start_message(client, message):
    bot_user = await client.get_me()
    bot_name = bot_user.first_name
    ping = round(time.time() - message.date.timestamp(), 2)
    uptime = get_uptime()

    caption = f"""🍃 ɢʀᴇᴇᴛɪɴɢs, ɪ'ᴍ {bot_name} 🫧, ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!
━━━━━━━▧▣▧━━━━━━━
⦾ ᴡʜᴀᴛ ɪ ᴅᴏ: ɪ sᴘᴀᴡɴ   
     ᴡᴀɪғᴜs ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ ғᴏʀ
     ᴜsᴇʀs ᴛᴏ ɢʀᴀʙ.
⦾ ᴛᴏ ᴜsᴇ ᴍᴇ: ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ
     ɢʀᴏᴜᴘ ᴀɴᴅ ᴛᴀᴘ ᴛʜᴇ ʜᴇʟᴩ
     ʙᴜᴛᴛᴏɴ ғᴏʀ ᴅᴇᴛᴀɪʟs.
━━━━━━━▧▣▧━━━━━━━
➺ ᴘɪɴɢ: {ping} ms
➺ ᴜᴘᴛɪᴍᴇ: {uptime}"""

    buttons = [
        [InlineKeyboardButton("Aᴅᴅ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ", url=f"https://t.me/{bot_user.username}?startgroup=true")],
        [InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT),
         InlineKeyboardButton("Cʜᴀɴɴᴇʟ", url=UPDATE_CHAT)],
        [InlineKeyboardButton("Hᴇʟᴘ", callback_data="open_help")],
        [InlineKeyboardButton(" 𓆰𝐎𝐰𝐧𝐞𝐫𓆪ꪾ", url=f"https://t.me/{OWNER_USERNAME}")]
    ]

    return caption, InlineKeyboardMarkup(buttons)

# 🔹 Function to Generate Group Start Message & Buttons
async def generate_group_start_message(client):
    bot_user = await client.get_me()
    caption = f"🍃 ɪ'ᴍ {bot_user.first_name} 🫧\nɪ sᴘᴀᴡɴ ᴡᴀɪғᴜs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ғᴏʀ ᴜsᴇʀs ᴛᴏ ɢʀᴀʙ.\nᴜsᴇ /help ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏ."
    buttons = [
        [InlineKeyboardButton("Aᴅᴅ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ", url=f"https://t.me/{bot_user.username}?startgroup=true")],
        [InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT),
         InlineKeyboardButton("Cʜᴀɴɴᴇʟ", url=UPDATE_CHAT)],
        [InlineKeyboardButton("Hᴇʟᴘ", callback_data="open_help")],
        [InlineKeyboardButton(" 𓆰𝐎𝐰𝐧𝐞𝐫𓆪ꪾ", url=f"https://t.me/{OWNER_USERNAME}")]
    ]
    return caption, InlineKeyboardMarkup(buttons)

# 🔹 Private Start Command Handler
@app.on_message(filters.command("start") & filters.private)
async def start_private_command(client, message):
    # Check if database collection is available before attempting database operations
    if user_collection is not None:
        try:
            existing_user = await user_collection.find_one({"id": message.from_user.id})
            if not existing_user:
                user_data = {
                    "id": message.from_user.id,
                    "username": message.from_user.username,
                    "first_name": message.from_user.first_name,
                    "last_name": message.from_user.last_name,
                    "start_time": time.time()
                }
                await user_collection.insert_one(user_data)
        except Exception as e:
            print(f"⚠️ Database error in start command: {e}")
    else:
        print("⚠️ Database collection not available, skipping user data storage")

    caption, buttons = await generate_start_message(client, message)
    try:
        media = random.choice(START_MEDIA)
        
        if GLOG and str(GLOG).strip():  # Check if GLOG is not empty
            await app.send_message(
                chat_id=GLOG,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"
                     f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                     f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )
    except ChatWriteForbidden:
        print(f"⚠️ Cannot send log to GLOG ({GLOG}) — No permission.")
    except Exception as e:
        print(f"⚠️ Logging error: {e}")
    
    # Handle case where media might be None or invalid
    if media and isinstance(media, str):
        if media.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            await message.reply_photo(photo=media, caption=caption, reply_markup=buttons)
        else:
            await message.reply_video(video=media, caption=caption, reply_markup=buttons)
    else:
        # Fallback to text message if media is invalid
        await message.reply_text(text=caption, reply_markup=buttons)

# 🔹 Group Start Command Handler
@app.on_message(filters.command("start") & filters.group)
async def start_group_command(client, message):
    caption, buttons = await generate_group_start_message(client)
    try:
        media = random.choice(START_MEDIA)
        
        # Handle case where media might be None or invalid
        if media and isinstance(media, str):
            if media.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                await message.reply_photo(photo=media, caption=caption, reply_markup=buttons)
            else:
                await message.reply_video(video=media, caption=caption, reply_markup=buttons)
        else:
            # Fallback to text message if media is invalid
            await message.reply_text(text=caption, reply_markup=buttons)
    except Exception as e:
        # Fallback to text message if media sending fails
        await message.reply_text(text=caption, reply_markup=buttons)

# 🔹 Function to Find Help Modules
def find_help_modules():
    buttons = []
    for module_name, module_data in HELP_DATA.items():
        button_name = module_data.get("HELP_NAME", "Unknown")
        buttons.append(InlineKeyboardButton(button_name, callback_data=f"help_{module_name}"))
    return [buttons[i:i + 3] for i in range(0, len(buttons), 3)]

# 🔹 Help Button Click Handler
@app.on_callback_query(filters.regex("^open_help$"))
async def show_help_menu(client, query: CallbackQuery):
    time.sleep(1)
    buttons = find_help_modules()
    buttons.append([InlineKeyboardButton("⬅ Back", callback_data="back_to_home")])
    await query.message.edit_text(
        """*ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.

ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /""",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# 🔹 Individual Module Help Handler
@app.on_callback_query(filters.regex(r"^help_(.+)"))
async def show_help(client, query: CallbackQuery):
    time.sleep(1)
    module_name = query.data.split("_", 1)[1]
    try:
        module_data = HELP_DATA.get(module_name, {})
        help_text = module_data.get("HELP", "Is module ka koi help nahi hai.")
        buttons = [[InlineKeyboardButton("⬅ Back", callback_data="open_help")]]
        await query.message.edit_text(f"**{module_name} Help:**\n\n{help_text}",
                                      reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await query.answer("Help load karne me error aayi!")

# 🔹 Back to Home
@app.on_callback_query(filters.regex("^back_to_home$"))
async def back_to_home(client, query: CallbackQuery):
    time.sleep(1)
    caption, buttons = await generate_start_message(client, query.message)
    await query.message.edit_text(caption, reply_markup=buttons)

# 🔹 Help Command Handler
@app.on_message(filters.command("help"))
async def help_command(client, message):
    buttons = find_help_modules()
    buttons.append([InlineKeyboardButton("⬅ Back", callback_data="back_to_home")])
    await message.reply_text(
        """*ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.

ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /""",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
