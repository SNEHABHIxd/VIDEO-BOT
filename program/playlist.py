# Copyright (C) 2021 By SNEHABHI VIDEO PLAYER
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

from config import BOT_USERNAME
from pyrogram.types import Message
from driver.filters import command, other_filters
from pyrogram import Client, filters
from driver.queues import QUEUE, get_queue


@Client.on_message(command(["playlist", f"playlist@SNEHABHI_VIDEOBOT", "queue", f"queue@SNEHABHI_VIDEOBOT"]) & other_filters)
async def playlist(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      chat_queue = get_queue(chat_id)
      if len(chat_queue)==1:
         await m.reply(f"💡 **𝙽𝙾𝚆 𝙿𝙻𝙰𝚈𝙸𝙽𝙶:**\n\n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`", disable_web_page_preview=True)
      else:
         QUE = f"💡 **𝙽𝙾𝚆 𝙿𝙻𝙰𝚈𝙸𝙽𝙶:**\n\n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**📖 𝙿𝙻𝙰𝚈-𝙻𝙸𝚂𝚃:**"
         l = len(chat_queue)
         for x in range (1, l):
            han = chat_queue[x][0]
            hok = chat_queue[x][2]
            hap = chat_queue[x][3]
            QUE = QUE + "\n" + f"**#{x}** - [{han}]({hok}) | `{hap}`"
         await m.reply(QUE, disable_web_page_preview=True)
   else:
      await m.reply("❌ **𝙽𝙾𝚃𝙷𝙸𝙽𝙶 𝙸𝚂 𝙲𝚄𝚁𝚁𝙴𝙽𝚃𝙻𝚈 𝚂𝚃𝚁𝙴𝙰𝙼𝙸𝙽𝙶.**")
