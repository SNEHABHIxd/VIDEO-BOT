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
        f"""β¨ **ππ΄π»π²πΎπΌπ΄ πΈ'πΌ ππ½π΄π·π°π±π·πΈ ππΈπ³π΄πΎ πΏπ»π°ππ΄π !**\n
π­ [ππ½π΄π·π°π±π·πΈ ππΈπ³π΄πΎ πΏπ»π°ππ΄π](https://t.me/SNEHABHI_VIDEOBOT) **π°π»π»πΎππ ππΎ πΏπ»π°π ππΈπ³π΄πΎ πΎπ½ πΆππΎππΏ'π ππΈπ³π΄πΎ π²π·π°π!**

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "πΆππΎππΏ πΌπ΄ π³π°π» π³π΄ π³π΄πΊπ· πΌπ",
                        url=f"https://t.me/SNEHABHI_VIDEOBOT?startgroup=true",
                    )
                ],
                
                [
                    InlineKeyboardButton(
                        "πΉπΎπΈπ½ πππΏπΏπΎππ", url=f"https://t.me/SNEHABHI_SERVER"
                    ),
                    InlineKeyboardButton(
                        "πΉπΎπΈπ½ π²π·π°π½π½π΄π»", url=f"https://t.me/SNEHABHI_UPDATES"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "ππ΄πΏπΎππΈππΎππ", "πΉπΎπΈπ½ @SNEHABHI_UPDATES ππ΄πΏπΎ πΏππ±π»πΈπ² ππΎπΎπ½"
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
                InlineKeyboardButton("πΉπΎπΈπ½ πππΏπΏπΎππ", url=f"https://t.me/SNEHABHI_SERVER"),
                InlineKeyboardButton(
                    "πΉπΎπΈπ½ π²π·π°π½π½π΄π»", url=f"https://t.me/SNEHABHI_UPDATES"
                ),
            ]
        ]
    )

    alive = f"**π·π΄π»π»πΎ {message.from_user.mention()}, i'm ππ½π΄π·π°π±π·πΈ ππΈπ³π΄πΎ πΏπ»π°ππ΄π**\n\nβ¨ π±πΎπ πΈπ ππΎππΊπΈπ½πΆ ππΌπΎπΎππ·π»π\nπ πΌπ πΎππ½π΄π: [β¨ππ½π΄π·π°π±π·πΈ πΎππ½π΄π π«](https://t.me/SNEHABHI_KING)\nβ¨ π±πΎπ ππ΄πππΈπΎπ½: `v{__version__}`\nπ πΏπππΎπΆππ°πΌ ππ΄πππΈπΎπ½: `{pyrover}`\nβ¨ πΏπ·πππ·πΎπ½ ππ΄πππΈπΎπ½: `{__python_version__}`\nπ πΏπππΆπ²π°π»π»π ππ΄πππΈπΎπ½: `{pytover.__version__}`\nβ¨ ππΏππΈπΌπ΄ πππ°πππ: `{uptime}`\n\n**ππ·π°π½πΊπ π΅πΎπ π°π³π³πΈπ½πΆ ππ½π΄π·π°π±π·πΈ ππΈπ³π΄πΎ πΏπ»π°ππ΄π πΉπΎπΈπ½ π²π·π°π½π½π΄π» @SNEHABHI_UPDATES** β€"

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
    await m_reply.edit_text("π `πΏπΎπ½πΆ πΉπΎπΈπ½ @SNEHABHI_UPDATRS!`\n" f"β‘οΈ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "π€π±πΎπ πππ°πππ:\n"
        f"β’ **ππΏππΈπΌπ΄:** `{uptime}`\n"
        f"β’ **πππ°ππ ππΈπΌπ΄:** `{START_TIME_ISO}`"
    )
