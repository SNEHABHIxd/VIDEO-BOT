# Copyright (C) 2021 By SNEHABHI VIDEO PLAYER
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

import asyncio
import re

from config import BOT_USERNAME, GROUP_SUPPORT, IMG_1, IMG_2, UPDATES_CHANNEL
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:70]
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["vplay", f"vplay@SNEHABHI_VIDEOBOT"]) & other_filters)
async def vplay(client, m: Message):

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

    replied = m.reply_to_message
    chat_id = m.chat.id
    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("📥 **𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙰𝚄𝙳𝙸𝙾...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» __only 720, 480, 360 allowed__ \n💡 **now streaming video in 720p**"
                    )

            if replied.video:
                songname = replied.video.file_name[:70]
            elif replied.document:
                songname = replied.document.file_name[:70]

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **𝚃𝚁𝙰𝙲𝙺 𝙰𝙳𝙳𝙴𝙳 𝚃𝙾 𝚃𝙷𝙴 𝚀𝚄𝙴𝚄𝙴**\n\n🏷 **𝙽𝙰𝙼𝙴:** [{songname}]({link})\n💭 **𝙲𝙷𝙰𝚃:** `{chat_id}`\n🎧 **𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙱𝚈:** {m.from_user.mention()}\n🔢 **𝙰𝚃 𝙿𝙾𝚂𝙸𝚃𝙸𝙾𝙽 »** `{pos}`",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), amaze),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"💡 **𝚂𝚃𝚁𝙴𝙰𝙼𝙸𝙽𝙶 𝚂𝚃𝙰𝚁𝚃𝙴𝙳.**\n\n🏷 **𝙽𝙰𝙼𝙴:** [{songname}]({link})\n💭 **𝙲𝙷𝙰𝚃:** `{chat_id}`\n💡 **𝚂𝚃𝙰𝚃𝚄𝚂:** `𝙿𝙻𝙰𝚈𝙸𝙽𝙶`\n🎧 **𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙱𝚈:** {m.from_user.mention()}",
                    reply_markup=keyboard,
                )
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» 𝚁𝙴𝙿𝙻𝚈 𝚃𝙾 𝙰𝙽 **𝚅𝙸𝙳𝙴𝙾 𝙵𝙸𝙻𝙴** 𝙾𝚁 **𝙶𝙸𝚅𝙴 𝚂𝙾𝙼𝙴𝚃𝙷𝙸𝙽𝙶 𝚃𝙾 𝚂𝙴𝙰𝚁𝙲𝙷.**"
                )
            else:
                loser = await m.reply("🔎 **𝚂𝙴𝙰𝚁𝙲𝙷𝙸𝙽𝙶...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **𝙽𝙾 𝚁𝙴𝚂𝚄𝙻𝚃𝚂 𝙵𝙾𝚄𝙽𝙳.**")
                else:
                    songname = search[0]
                    url = search[1]
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await loser.edit(f"❌ 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳 𝙸𝚂𝚂𝚄𝙴 𝙳𝙴𝚃𝙴𝙲𝚃𝙴𝙳\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            await m.reply_photo(
                                photo=f"{IMG_1}",
                                caption=f"💡 **𝚃𝚁𝙰𝙲𝙺 𝙰𝙳𝙳𝙴𝙳 𝚃𝙾 𝚃𝙷𝙴 𝚀𝚄𝙴𝚄𝙴**\n\n🏷 **𝙽𝙰𝙼𝙴:** [{songname}]({url})\n💭 **𝙲𝙷𝙰𝚃:** `{chat_id}`\n🎧 **𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙱𝚈:** {m.from_user.mention()}\n🔢 **𝙰𝚃 𝙿𝙾𝚂𝙸𝚃𝙸𝙾𝙽 »** `{pos}`",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(ytlink, HighQualityAudio(), amaze),
                                    stream_type=StreamType().pulse_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                await m.reply_photo(
                                    photo=f"{IMG_2}",
                                    caption=f"💡 **𝚅𝙸𝙳𝙴𝙾 𝚂𝚃𝚁𝙴𝙰𝙼𝙸𝙽𝙶 𝚂𝚃𝙰𝚁𝚃𝙴𝙳.**\n\n🏷 **𝙽𝙰𝙼𝙴:** [{songname}]({url})\n💭 **𝙲𝙷𝙰𝚃** `{chat_id}`\n💡 **𝚂𝚃𝙰𝚃𝚄𝚂:** `𝙿𝙻𝙰𝚈𝙸𝙽𝙶`\n🎧 **𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙱𝚈:** {m.from_user.mention()}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» 𝚁𝙴𝙿𝙻𝚈 𝚃𝙾 𝙰𝙽 **𝚅𝙸𝙳𝙴𝙾 𝙵𝙸𝙻𝙴** 𝙾𝚁 **𝙶𝙸𝚅𝙴 𝚂𝙾𝙼𝙴𝚃𝙷𝙸𝙽𝙶 𝚃𝙾 𝚂𝙴𝙰𝚁𝙲𝙷.**"
            )
        else:
            loser = await m.reply("🔎 **𝚂𝙴𝙰𝚁𝙲𝙷𝙸𝙽𝙶...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **𝙽𝙾 𝚁𝙴𝚂𝚄𝙻𝚃𝚂 𝙵𝙾𝚄𝙽𝙳.**")
            else:
                songname = search[0]
                url = search[1]
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"❌ 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳 𝙸𝚂𝚂𝚄𝙴 𝙳𝙴𝚃𝙴𝙲𝚃𝙴𝙳\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        await m.reply_photo(
                            photo=f"{IMG_1}",
                            caption=f"💡 **𝚃𝚁𝙰𝙲𝙺 𝙰𝙳𝙳𝙴𝙳 𝚃𝙾 𝚃𝙷𝙴 𝚀𝚄𝙴𝚄𝙴**\n\n🏷 **Name:** [{songname}]({url})\n💭 **Chat:** `{chat_id}`\n🎧 **𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙱𝚈:** {m.from_user.mention()}\n🔢 **At position »** `{pos}`",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(ytlink, HighQualityAudio(), amaze),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            await m.reply_photo(
                                photo=f"{IMG_2}",
                                caption=f"💡 **𝚅𝙸𝙳𝙴𝙾 𝚂𝚃𝚁𝙴𝙰𝙼𝙸𝙽𝙶 𝚂𝚃𝙰𝚁𝚃𝙴𝙳.**\n\n🏷 **𝙽𝙰𝙼𝙴:** [{songname}]({url})\n💭 **𝙲𝙷𝙰𝚃:** `{chat_id}`\n💡 **𝚂𝚃𝙰𝚃𝚄𝚂:** `𝙿𝙻𝙰𝚈𝙸𝙽𝙶`\n🎧 **𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙱𝚈:** {m.from_user.mention()}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await m.reply_text(f"🚫 𝙴𝚁𝚁𝙾𝚁: `{ep}`")


@Client.on_message(command(["vstream", f"vstream@SNEHABHI_VIDEOBOT"]) & other_filters)

async def vstream(client, m: Message):

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
        await m.reply("» give me a live-link/m3u8 url/youtube link to stream.")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await m.reply("🔄 **𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙸𝙽𝙶 𝚂𝚃𝚁𝙴𝙰𝙼 @SNEHABHI_UPDATES...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» __only 720, 480, 360 allowed__ \n💡 **now streaming video in 720p**"
                )
            loser = await m.reply("🔄 **𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙸𝙽𝙶 𝚂𝚃𝚁𝙴𝙰𝙼 @SNEHABHI_UPDATES...**")
        else:
            await m.reply("**/vstream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await loser.edit(f"❌ 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳 𝙸𝚂𝚂𝚄𝙴 𝙳𝙴𝚃𝙴𝙲𝚃𝙴𝙳\n\n» `{ytlink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **𝚃𝚁𝙰𝙲𝙺 𝙰𝙳𝙳𝙴𝙳 𝚃𝙾 𝚃𝙷𝙴 𝚀𝚄𝙴𝚄𝙴**\n\n💭 **𝙲𝙷𝙰𝚃:** `{chat_id}`\n🎧 **𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙱𝚈:** {m.from_user.mention()}\n🔢 **𝙰𝚃 𝙿𝙾𝚂𝙸𝚃𝙸𝙾𝙽 »** `{pos}`",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(livelink, HighQualityAudio(), amaze),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"💡 **[Live stream video]({link}) started.**\n\n💭 **𝙲𝙷𝙰𝚃:** `{chat_id}`\n💡 **Status:** `Playing`\n🎧 **𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙱𝚈:** {m.from_user.mention()}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await m.reply_text(f"🚫 𝙴𝚁𝚁𝙾𝚁: `{ep}`")
