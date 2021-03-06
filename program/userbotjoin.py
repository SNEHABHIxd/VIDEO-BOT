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
            "β’ **πΈ'πΌ π½πΎπ π·π°ππ΄ πΏπ΄ππΌπΈπππΈπΎπ½:**\n\nΒ» β __π°π³π³ πππ΄ππ__",
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
            f"π Flood Wait Error π \n\n**userbot couldn't join your group due to heavy join requests for userbot**"
            "\n\n**or add assistant manually to your Group and try again**",
        )
        return
    await message.reply_text(
        f"β **ππ½π΄π·π°π±π·πΈ πππ΄ππ±πΎπ πππ²π²π΄πππ΅ππ»π»π πΉπΎπΈπ½π΄π³ ππ·π΄ πΆππΎππΏ**",
    )


@Client.on_message(command(["userbotleave",
                            f"leave@SNEHABHI_VIDEOBOT"]) & filters.group & ~filters.edited)
@authorized_users_only
async def leave_one(client, message):
    try:
        await USER.send_message(message.chat.id, "β ππ½π΄π·π°π±π·πΈ πππ΄ππ±πΎπ πππ²π²π΄πππ΅ππ»π»π π»π΄π΅π ππ·π΄ πΆππΎππΏ")
        await USER.leave_chat(message.chat.id)
    except BaseException:
        await message.reply_text(
            "β **ππ½π΄π·π°π±π·πΈ πππ΄ππ±πΎπ π²πΎππ»π³π½'π π»π΄π°ππ΄ ππΎππ πΆππΎππΏ, πΌπ°π π±π΄ π΅π»πΎπΎπ³ππ°πΈππ.**\n\n**Β» πΎπ πΌπ°π½ππ°π»π»π πΊπΈπ²πΊ ππ½π΄π·π°π±π·πΈ πππ΄ππ±πΎπ π΅ππΎπΌ ππΎππ πΆππΎππΏ**"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@SNEHABHI_VIDEOBOT"]))
@sudo_users_only
async def leave_all(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("π **ππ½π΄π·π°π±π·πΈ πππ΄ππ±πΎπ** π»π΄π°ππΈπ½πΆ π°π»π» πΆππΎππΏπ !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"ππ½π΄π·π°π±π·πΈ πππ΄ππ±πΎπ π»π΄π°ππΈπ½πΆ π°π»π» πΆππΎππΏπ...\n\nπ»π΄π΅π: {left} π²π·π°ππ.\nπ΅π°πΈπ»π΄π³: {failed} π²π·π°ππ."
            )
        except BaseException:
            failed += 1
            await lol.edit(
                f"Userbot leaving...\n\nπ»π΄π΅π: {left} π²π·π°ππ.\nπ΅π°πΈπ»π΄π³: {failed} π²π·π°ππ."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"β π»π΄π΅π π΅ππΎπΌ: {left} π²π·π°ππ.\nβ π΅π°πΈπ»π΄π³ πΈπ½: {failed} π²π·π°ππ."
    )
