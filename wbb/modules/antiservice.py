# Written By [MaskedVirus | swatv3nub] for William and Ryūga
# Kang With Proper Credits

from pyrogram import filters

from wbb import app
from wbb.core.decorators.permissions import adminsOnly
from wbb.utils.dbfunctions import (antiservice_off, antiservice_on,
                                   is_antiservice_on)

__MODULE__ = "AntiService"
__HELP__ = """
ᴘʟᴜɢɪɴ ᴛᴏ ᴅᴇʟᴇᴛᴇ ꜱᴇʀᴠɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇꜱ ɪɴ ᴀ ᴄʜᴀᴛ 🍔

/antiservice [enable|disable]
"""


@app.on_message(filters.command("antiservice") & ~filters.private)
@adminsOnly("can_change_info")
async def anti_service(_, message):
    if len(message.command) != 2:
        return await message.reply_text(
            "Usage: /antiservice [enable | disable]"
        )
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "enable":
        await antiservice_on(chat_id)
        await message.reply_text(
            "ᴇɴᴀʙʟᴇᴅ ᴀɴᴛɪꜱᴇʀᴠɪᴄᴇ ꜱʏꜱᴛᴇᴍ. ɪ ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ꜱᴇʀᴠɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇꜱ ꜰʀᴏᴍ ɴᴏᴡ ᴏɴ.✅"
        )
    elif status == "disable":
        await antiservice_off(chat_id)
        await message.reply_text(
            "ᴅɪꜱᴀʙʟᴇᴅ ᴀɴᴛɪꜱᴇʀᴠɪᴄᴇ ꜱʏꜱᴛᴇᴍ. ɪ ᴡᴏɴ'ᴛ ʙᴇ ᴅᴇʟᴇᴛɪɴɢ ꜱᴇʀᴠɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇ ꜰʀᴏᴍ ɴᴏᴡ ᴏɴ.⚠️"
        )
    else:
        await message.reply_text(
            "ᴜɴᴋɴᴏᴡɴ ꜱᴜꜰꜰɪx, ᴜꜱᴇ /antiservice [enable|disable]"
        )


@app.on_message(filters.service, group=11)
async def delete_service(_, message):
    chat_id = message.chat.id
    try:
        if await is_antiservice_on(chat_id):
            return await message.delete()
    except Exception:
        pass
