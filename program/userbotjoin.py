import asyncio
from config import BOT_USERNAME, SUDO_USERS
from driver.decorators import authorized_users_only, sudo_users_only, errors
from driver.filters import command, other_filters
from driver.snehabhi import user as USER
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command(["userbotjoin", f"userbotjoin@SNEHABHI_VIDEOBOT"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def join_group(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except BaseException:
        await message.reply_text(
            "• **𝙸'𝙼 𝙽𝙾𝚃 𝙷𝙰𝚅𝙴 𝙿𝙴𝚁𝙼𝙸𝚂𝚂𝙸𝙾𝙽:**\n\n» ❌ __𝙰𝙳𝙳 𝚄𝚂𝙴𝚁𝚂__",
        )
        return

    try:
        user = await USER.get_me()
    except BaseException:
        user.first_name = "music assistant"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        print(e)
        await message.reply_text(
            f"🛑 Flood Wait Error 🛑 \n\n**userbot couldn't join your group due to heavy join requests for userbot**"
            "\n\n**or add assistant manually to your Group and try again**",
        )
        return
    await message.reply_text(
        f"✅ **𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙹𝙾𝙸𝙽𝙴𝙳 𝚃𝙷𝙴 𝙶𝚁𝙾𝚄𝙿**",
    )


@Client.on_message(command(["userbotleave",
                            f"leave@SNEHABHI_VIDEOBOT"]) & filters.group & ~filters.edited)
@authorized_users_only
async def leave_one(client, message):
    try:
        await USER.send_message(message.chat.id, "✅ 𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙻𝙴𝙵𝚃 𝚃𝙷𝙴 𝙶𝚁𝙾𝚄𝙿")
        await USER.leave_chat(message.chat.id)
    except BaseException:
        await message.reply_text(
            "❌ **𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 𝙲𝙾𝚄𝙻𝙳𝙽'𝚃 𝙻𝙴𝙰𝚅𝙴 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿, 𝙼𝙰𝚈 𝙱𝙴 𝙵𝙻𝙾𝙾𝙳𝚆𝙰𝙸𝚃𝚂.**\n\n**» 𝙾𝚁 𝙼𝙰𝙽𝚄𝙰𝙻𝙻𝚈 𝙺𝙸𝙲𝙺 𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 𝙵𝚁𝙾𝙼 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿**"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@SNEHABHI_VIDEOBOT"]))
@sudo_users_only
async def leave_all(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚄𝚂𝙴𝚁𝙱𝙾𝚃** 𝙻𝙴𝙰𝚅𝙸𝙽𝙶 𝙰𝙻𝙻 𝙶𝚁𝙾𝚄𝙿𝚂 !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 𝙻𝙴𝙰𝚅𝙸𝙽𝙶 𝙰𝙻𝙻 𝙶𝚁𝙾𝚄𝙿𝚂...\n\n𝙻𝙴𝙵𝚃: {left} 𝙲𝙷𝙰𝚃𝚂.\n𝙵𝙰𝙸𝙻𝙴𝙳: {failed} 𝙲𝙷𝙰𝚃𝚂."
            )
        except BaseException:
            failed += 1
            await lol.edit(
                f"Userbot leaving...\n\n𝙻𝙴𝙵𝚃: {left} 𝙲𝙷𝙰𝚃𝚂.\n𝙵𝙰𝙸𝙻𝙴𝙳: {failed} 𝙲𝙷𝙰𝚃𝚂."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"✅ 𝙻𝙴𝙵𝚃 𝙵𝚁𝙾𝙼: {left} 𝙲𝙷𝙰𝚃𝚂.\n❌ 𝙵𝙰𝙸𝙻𝙴𝙳 𝙸𝙽: {failed} 𝙲𝙷𝙰𝚃𝚂."
    )
