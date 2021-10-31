from cache.admins import admins
from driver.veez import call_py
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
        "✅ 𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚅𝙸𝙳𝙴𝙾 𝙿𝙻𝙰𝚈𝙴𝚁 **𝚁𝙴𝙻𝙾𝙰𝙳𝙴𝙳 𝙲𝙾𝚁𝚁𝙴𝙲𝚃𝙻𝚈 !**\n✅ **𝙰𝙳𝙼𝙸𝙽 𝙻𝙸𝚂𝚃** 𝙷𝙰𝚂 𝙱𝙴𝙴𝙽 **𝚄𝙿𝙳𝙰𝚃𝙴S 𝙱𝚈 @SNEHABHI_UPDATES !**"
    )


@Client.on_message(command(["skip", f"skip@SNEHABHI_VIDEOBOT", "vskip"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="✨ ɢʀᴏᴜᴘ", url=f"https://t.me/SNEHABHI_SERVER"
                ),
                InlineKeyboardButton(
                    text="🌻 ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/SNEHABHI_UPDATES"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ 𝙽𝙾𝚃𝙷𝙸𝙽𝙶 𝙸𝚂 𝙲𝚄𝚁𝚁𝙴𝙽𝚃𝙻𝚈 𝙿𝙻𝙰𝚈𝙸𝙽𝙶")
        elif op == 1:
            await m.reply("✅ __𝚀𝚄𝙴𝚄𝙴𝚂__ 𝙸𝚂 𝙴𝙼𝙿𝚃𝚈.\n\n• 𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 𝙻𝙴𝙰𝚅𝙸𝙽𝙶 𝚅𝙲")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"⏭ **𝚂𝙺𝙸𝙿𝙿𝙴𝙳 𝚃𝙾 𝚃𝙷𝙴 𝙽𝙴𝚇𝚃 𝚃𝚁𝙰𝙲𝙺.**\n\n🏷 **𝙽𝙰𝙼𝙴:** [{op[0]}]({op[1]})\n💭 **𝙲𝙷𝙰𝚃:** `{chat_id}`\n💡 **𝚂𝚃𝙰𝚃𝚄𝚂:** `𝙿𝙻𝙰𝚈𝙸𝙽𝙶`\n🎧 **𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙱𝚈:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **removed song from queue:**"
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
            await m.reply("✅ **𝚂𝚃𝚁𝙴𝙰𝙼𝙸𝙽𝙶 𝙷𝙰𝚂 𝙴𝙽𝙳𝙴𝙳 𝚄𝙿𝙻𝙾𝙰𝙳 𝙱𝚈 @SNEHABHI_UPDATES.**")
        except Exception as e:
            await m.reply(f"🚫 **𝙴𝚁𝚁𝙾𝚁:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝙽𝙾𝚃𝙷𝙸𝙽𝙶 𝙸𝙽 𝚂𝚃𝚁𝙴𝙰𝙼𝙸𝙽𝙶 𝚄𝙿𝙻𝙾𝙰𝙳 𝙱𝚈 @SNEHABHI_UPDATES**")


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
                "⏸ **𝚃𝚁𝙰𝙲𝙺 𝙿𝙰𝚄𝚂𝙴.**\n\n• **𝚃𝙾 𝚁𝙴𝚂𝚄𝙼𝙴 𝚃𝙷𝙴 𝚂𝚃𝚁𝙴𝙰𝙼 , 𝚄𝚂𝙴 𝚃𝙷𝙴**\n» /resume 𝙲𝙾𝙼𝙼𝙰𝙽𝙳."
            )
        except Exception as e:
            await m.reply(f"🚫 **𝙴𝚁𝚁𝙾𝚁:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝙽𝙾𝚃𝙷𝙸𝙽𝙶 𝙸𝙽 𝚂𝚃𝚁𝙴𝙰𝙼𝙸𝙽𝙶 𝚄𝙿𝙻𝙾𝙰𝙳 𝙱𝚈 @SNEHABHI_UPDATES**")


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
                "▶️ **𝚃𝚁𝙰𝙲𝙺 𝚁𝙴𝚂𝚄𝙼𝙴.**\n\n• **𝚃𝙾 𝙿𝙰𝚄𝚂𝙴 𝚃𝙷𝙴 𝚂𝚃𝚁𝙴𝙰𝙼 , 𝚄𝚂𝙴 𝚃𝙷𝙴**\n» /pause 𝙲𝙾𝙼𝙼𝙰𝙽𝙳."
            )
        except Exception as e:
            await m.reply(f"🚫 **𝙴𝚁𝚁𝙾𝚁:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝙽𝙾𝚃𝙷𝙸𝙽𝙶 𝙸𝙽 𝚂𝚃𝚁𝙴𝙰𝙼𝙸𝙽𝙶 𝚄𝙿𝙻𝙾𝙰𝙳 𝙱𝚈 @SNEHABHI_UPDATES**")


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
                "🔇 **𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 𝙼𝚄𝚃𝙴𝙳.**\n\n• **𝚃𝙾 𝚄𝙽𝙼𝚄𝚃𝙴 𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 , 𝚄𝚂𝙴 𝚃𝙷𝙴**\n» /unmute 𝙲𝙾𝙼𝙼𝙰𝙽𝙳."
            )
        except Exception as e:
            await m.reply(f"🚫 **𝙴𝚁𝚁𝙾𝚁:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝙽𝙾𝚃𝙷𝙸𝙽𝙶 𝙸𝙽 𝚂𝚃𝚁𝙴𝙰𝙼𝙸𝙽𝙶 𝚄𝙿𝙻𝙾𝙰𝙳 𝙱𝚈 @SNEHABHI_UPDATES**")


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
                "🔊 **𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 𝚄𝙽𝙼𝚄𝚃𝙴D.**\n\n• **𝚃𝙾 𝙼𝚄𝚃𝙴𝙳 𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 , 𝚄𝚂𝙴 𝚃𝙷𝙴**\n» /mute 𝙲𝙾𝙼𝙼𝙰𝙽𝙳."
            )
        except Exception as e:
            await m.reply(f"🚫 **𝙴𝚁𝚁𝙾𝚁:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝙽𝙾𝚃𝙷𝙸𝙽𝙶 𝙸𝙽 𝚂𝚃𝚁𝙴𝙰𝙼𝙸𝙽𝙶 𝚄𝙿𝙻𝙾𝙰𝙳 𝙱𝚈 @SNEHABHI_UPDATES**")


@Client.on_message(
    command(["volume", f"volume@SNEHABHI_VIDEOBOT", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    try:
        await call_py.change_volume_call(chat_id, volume=int(range))
        await m.reply(f"✅ **𝚅𝙾𝙻𝚄𝙼𝙴 𝚂𝙴𝚃 𝚃𝙾** `{range}`%")
    except Exception as e:
        await m.reply(f"🚫 **𝙴𝚁𝚁𝙾𝚁:**\n\n{e}")
