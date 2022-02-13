from pyrogram import filters
from pyrogram.types import Message

from wbb import SUDOERS, app
from wbb.core.decorators.errors import capture_err
from wbb.utils.dbfunctions import (blacklist_chat, blacklisted_chats,
                                   whitelist_chat)

__MODULE__ = "Blacklist Chat"
__HELP__ = """
**THIS MODULE IS ONLY FOR DEVS**

ᴜꜱᴇ ᴛʜɪꜱ ᴍᴏᴅᴜʟᴇ ᴛᴏ ᴍᴀᴋᴇ ᴛʜᴇ ʙᴏᴛ ʟᴇᴀᴠᴇ ꜱᴏᴍᴇ ᴄʜᴀᴛꜱ
ɪɴ ᴡʜɪᴄʜ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴡᴀɴᴛ ɪᴛ ᴛᴏ ʙᴇ ɪɴ.

/blacklist_chat [CHAT_ID] - ʙʟᴀᴄᴋʟɪꜱᴛ ᴀ ᴄʜᴀᴛ.
/whitelist_chat [CHAT_ID] - ᴡʜɪᴛᴇʟɪꜱᴛ ᴀ ᴄʜᴀᴛ.
/blacklisted - ꜱʜᴏᴡ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴄʜᴀᴛꜱ.
"""


@app.on_message(filters.command("blacklist_chat") & filters.user(SUDOERS))
@capture_err
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:**\n/blacklist_chat [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text("ᴄʜᴀᴛ ɪꜱ ᴀʟʀᴇᴀᴅʏ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ.")
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        return await message.reply_text(
            "ᴄʜᴀᴛ ʜᴀꜱ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ"
        )
    await message.reply_text("ꜱᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ, ᴄʜᴇᴄᴋ ʟᴏɢꜱ.")


@app.on_message(filters.command("whitelist_chat") & filters.user(SUDOERS))
@capture_err
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:**\n/whitelist_chat [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text("ᴄʜᴀᴛ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴡʜɪᴛᴇʟɪꜱᴛᴇᴅ.")
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(
            "ᴄʜᴀᴛ ʜᴀꜱ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴡʜɪᴛᴇʟɪꜱᴛᴇᴅ"
        )
    await message.reply_text("ꜱᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ, ᴄʜᴇᴄᴋ ʟᴏɢꜱ.")


@app.on_message(filters.command("blacklisted_chats") & filters.user(SUDOERS))
@capture_err
async def blacklisted_chats_func(_, message: Message):
    text = ""
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception:
            title = "Private"
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    await message.reply_text(text)
