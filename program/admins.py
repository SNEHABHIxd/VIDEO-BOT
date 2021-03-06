from cache.admins import admins
from driver.snehabhi import call_py
from pyrogram import Client, filters
from driver.decorators import authorized_users_only
from driver.filters import command, other_filters
from driver.queues import QUEUE, clear_queue
from driver.utils import skip_current_song, skip_item
from config import BOT_USERNAME, GROUP_SUPPORT, IMG_3, UPDATES_CHANNEL
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@Client.on_message(command(["reload", f"reload@SNEHABHI_VIDEOBOT"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "β ππ½π΄π·π°π±π·πΈ ππΈπ³π΄πΎ πΏπ»π°ππ΄π **ππ΄π»πΎπ°π³π΄π³ π²πΎπππ΄π²ππ»π !**\nβ **π°π³πΌπΈπ½ π»πΈππ** π·π°π π±π΄π΄π½ **ππΏπ³π°ππ΄S π±π @SNEHABHI_UPDATES !**"
    )


@Client.on_message(command(["skip", f"skip@SNEHABHI_VIDEOBOT", "vskip"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="β¨ Ι’Κα΄α΄α΄", url=f"https://t.me/SNEHABHI_SERVER"
                ),
                InlineKeyboardButton(
                    text="π» α΄Κα΄Ι΄Ι΄α΄Κ", url=f"https://t.me/SNEHABHI_UPDATES"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("β π½πΎππ·πΈπ½πΆ πΈπ π²ππππ΄π½ππ»π πΏπ»π°ππΈπ½πΆ")
        elif op == 1:
            await m.reply("β __πππ΄ππ΄π__ πΈπ π΄πΌπΏππ.\n\nβ’ ππ½π΄π·π°π±π·πΈ πππ΄ππ±πΎπ π»π΄π°ππΈπ½πΆ ππ²")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"β­ **ππΊπΈπΏπΏπ΄π³ ππΎ ππ·π΄ π½π΄ππ πππ°π²πΊ.**\n\nπ· **π½π°πΌπ΄:** [{op[0]}]({op[1]})\nπ­ **π²π·π°π:** `{chat_id}`\nπ‘ **πππ°πππ:** `πΏπ»π°ππΈπ½πΆ`\nπ§ **ππ΄πππ΄ππ π±π:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "π **removed song from queue:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["stop", f"stop@SNEHABHI_VIDEOBOT", "end", f"end@SNEHABHI_VIDEOBOT", "vstop"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("β **ππππ΄π°πΌπΈπ½πΆ π·π°π π΄π½π³π΄π³ ππΏπ»πΎπ°π³ π±π @SNEHABHI_UPDATES.**")
        except Exception as e:
            await m.reply(f"π« **π΄πππΎπ:**\n\n`{e}`")
    else:
        await m.reply("β **π½πΎππ·πΈπ½πΆ πΈπ½ ππππ΄π°πΌπΈπ½πΆ ππΏπ»πΎπ°π³ π±π @SNEHABHI_UPDATES**")


@Client.on_message(
    command(["pause", f"pause@SNEHABHI_VIDEOBOT", "vpause"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "βΈ **πππ°π²πΊ πΏπ°πππ΄.**\n\nβ’ **ππΎ ππ΄πππΌπ΄ ππ·π΄ ππππ΄π°πΌ , πππ΄ ππ·π΄**\nΒ» /resume π²πΎπΌπΌπ°π½π³."
            )
        except Exception as e:
            await m.reply(f"π« **π΄πππΎπ:**\n\n`{e}`")
    else:
        await m.reply("β **π½πΎππ·πΈπ½πΆ πΈπ½ ππππ΄π°πΌπΈπ½πΆ ππΏπ»πΎπ°π³ π±π @SNEHABHI_UPDATES**")


@Client.on_message(
    command(["resume", f"resume@SNEHABHI_VIDEOBOT", "vresume"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "βΆοΈ **πππ°π²πΊ ππ΄πππΌπ΄.**\n\nβ’ **ππΎ πΏπ°πππ΄ ππ·π΄ ππππ΄π°πΌ , πππ΄ ππ·π΄**\nΒ» /pause π²πΎπΌπΌπ°π½π³."
            )
        except Exception as e:
            await m.reply(f"π« **π΄πππΎπ:**\n\n`{e}`")
    else:
        await m.reply("β **π½πΎππ·πΈπ½πΆ πΈπ½ ππππ΄π°πΌπΈπ½πΆ ππΏπ»πΎπ°π³ π±π @SNEHABHI_UPDATES**")


@Client.on_message(
    command(["mute", f"mute@SNEHABHI_VIDEOBOT", "vmute"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "π **ππ½π΄π·π°π±π·πΈ πππ΄ππ±πΎπ πΌπππ΄π³.**\n\nβ’ **ππΎ ππ½πΌπππ΄ ππ½π΄π·π°π±π·πΈ πππ΄ππ±πΎπ , πππ΄ ππ·π΄**\nΒ» /unmute π²πΎπΌπΌπ°π½π³."
            )
        except Exception as e:
            await m.reply(f"π« **π΄πππΎπ:**\n\n`{e}`")
    else:
        await m.reply("β **π½πΎππ·πΈπ½πΆ πΈπ½ ππππ΄π°πΌπΈπ½πΆ ππΏπ»πΎπ°π³ π±π @SNEHABHI_UPDATES**")


@Client.on_message(
    command(["unmute", f"unmute@SNEHABHI_VIDEOBOT", "vunmute"]) & other_filters
)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "π **ππ½π΄π·π°π±π·πΈ πππ΄ππ±πΎπ ππ½πΌπππ΄D.**\n\nβ’ **ππΎ πΌπππ΄π³ ππ½π΄π·π°π±π·πΈ πππ΄ππ±πΎπ , πππ΄ ππ·π΄**\nΒ» /mute π²πΎπΌπΌπ°π½π³."
            )
        except Exception as e:
            await m.reply(f"π« **π΄πππΎπ:**\n\n`{e}`")
    else:
        await m.reply("β **π½πΎππ·πΈπ½πΆ πΈπ½ ππππ΄π°πΌπΈπ½πΆ ππΏπ»πΎπ°π³ π±π @SNEHABHI_UPDATES**")


@Client.on_message(
    command(["volume", f"volume@SNEHABHI_VIDEOBOT", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    try:
        await call_py.change_volume_call(chat_id, volume=int(range))
        await m.reply(f"β **ππΎπ»ππΌπ΄ ππ΄π ππΎ** `{range}`%")
    except Exception as e:
        await m.reply(f"π« **π΄πππΎπ:**\n\n{e}")
