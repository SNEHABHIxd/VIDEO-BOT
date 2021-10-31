from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from program import __version__
from driver.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@SNEHABHI_VIDEOBOT"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""✨ **𝚆𝙴𝙻𝙲𝙾𝙼𝙴 𝙸'𝙼 𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚅𝙸𝙳𝙴𝙾 𝙿𝙻𝙰𝚈𝙴𝚁 !**\n
💭 [𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚅𝙸𝙳𝙴𝙾 𝙿𝙻𝙰𝚈𝙴𝚁](https://t.me/SNEHABHI_VIDEOBOT) **𝙰𝙻𝙻𝙾𝚆𝚂 𝚃𝙾 𝙿𝙻𝙰𝚈 𝚅𝙸𝙳𝙴𝙾 𝙾𝙽 𝙶𝚁𝙾𝚄𝙿'𝚂 𝚅𝙸𝙳𝙴𝙾 𝙲𝙷𝙰𝚃!**

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝙶𝚁𝙾𝚄𝙿 𝙼𝙴 𝙳𝙰𝙻 𝙳𝙴 𝙳𝙴𝙺𝙷 𝙼𝚃",
                        url=f"https://t.me/SNEHABHI_VIDEOBOT?startgroup=true",
                    )
                ],
                
                [
                    InlineKeyboardButton(
                        "𝙹𝙾𝙸𝙽 𝚂𝚄𝙿𝙿𝙾𝚁𝚃", url=f"https://t.me/SNEHABHI_SERVER"
                    ),
                    InlineKeyboardButton(
                        "𝙹𝙾𝙸𝙽 𝙲𝙷𝙰𝙽𝙽𝙴𝙻", url=f"https://t.me/SNEHABHI_UPDATES"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "𝚁𝙴𝙿𝙾𝚂𝙸𝚃𝙾𝚁𝚈", "𝙹𝙾𝙸𝙽 @SNEHABHI_UPDATES 𝚁𝙴𝙿𝙾 𝙿𝚄𝙱𝙻𝙸𝙲 𝚂𝙾𝙾𝙽"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["alive", f"alive@SNEHABHI_VIDEOBOT"]) & filters.group & ~filters.edited
)
async def alive(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("𝙹𝙾𝙸𝙽 𝚂𝚄𝙿𝙿𝙾𝚁𝚃", url=f"https://t.me/SNEHABHI_SERVER"),
                InlineKeyboardButton(
                    "𝙹𝙾𝙸𝙽 𝙲𝙷𝙰𝙽𝙽𝙴𝙻", url=f"https://t.me/SNEHABHI_UPDATES"
                ),
            ]
        ]
    )

    alive = f"**𝙷𝙴𝙻𝙻𝙾 {message.from_user.mention()}, i'm 𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚅𝙸𝙳𝙴𝙾 𝙿𝙻𝙰𝚈𝙴𝚁**\n\n✨ 𝙱𝙾𝚃 𝙸𝚂 𝚆𝙾𝚁𝙺𝙸𝙽𝙶 𝚂𝙼𝙾𝙾𝚃𝙷𝙻𝚈\n🍀 𝙼𝚈 𝙾𝚆𝙽𝙴𝚁: [✨𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝙾𝚆𝙽𝙴𝚁 💫](https://t.me/SNEHABHI_KING)\n✨ 𝙱𝙾𝚃 𝚅𝙴𝚁𝚂𝙸𝙾𝙽: `v{__version__}`\n🍀 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚅𝙴𝚁𝚂𝙸𝙾𝙽: `{pyrover}`\n✨ 𝙿𝙷𝚈𝚃𝙷𝙾𝙽 𝚅𝙴𝚁𝚂𝙸𝙾𝙽: `{__python_version__}`\n🍀 𝙿𝚈𝚃𝙶𝙲𝙰𝙻𝙻𝚂 𝚅𝙴𝚁𝚂𝙸𝙾𝙽: `{pytover.__version__}`\n✨ 𝚄𝙿𝚃𝙸𝙼𝙴 𝚂𝚃𝙰𝚃𝚄𝚂: `{uptime}`\n\n**𝚃𝙷𝙰𝙽𝙺𝚂 𝙵𝙾𝚁 𝙰𝙳𝙳𝙸𝙽𝙶 𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚅𝙸𝙳𝙴𝙾 𝙿𝙻𝙰𝚈𝙴𝚁 𝙹𝙾𝙸𝙽 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 @SNEHABHI_UPDATES** ❤"

    await message.reply_photo(
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping", f"ping@SNEHABHI_VIDEOBOT"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `𝙿𝙾𝙽𝙶 𝙹𝙾𝙸𝙽 @SNEHABHI_UPDATRS!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖𝙱𝙾𝚃 𝚂𝚃𝙰𝚃𝚄𝚂:\n"
        f"• **𝚄𝙿𝚃𝙸𝙼𝙴:** `{uptime}`\n"
        f"• **𝚂𝚃𝙰𝚁𝚃 𝚃𝙸𝙼𝙴:** `{START_TIME_ISO}`"
    )
