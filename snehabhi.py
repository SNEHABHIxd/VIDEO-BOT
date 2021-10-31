import asyncio

from driver.snehabhi import bot, call_py
from pytgcalls import idle


async def mulai_bot():
    print("[INFO]: STARTING BOT CLIENT")
    await bot.start()
    print("[INFO]: STARTING PYTGCALLS CLIENT")
    await call_py.start()
    await idle()
    print("[INFO]: STOPPING BOT")
    await bot.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(mulai_bot())


print("𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝚅𝙸𝙳𝙴𝙾 𝙿𝙻𝙰𝚈𝙴𝚁 𝙱𝙾𝚃 𝙸𝚂 𝚂𝚃𝙰𝚁𝚃𝙴𝙳")
print("¯\_(ツ)_/¯ 𝙽𝙴𝙴𝙳 𝙷𝙴𝙻𝙿 𝙹𝙾𝙸𝙽 @SNEHABHI_SERVER")
