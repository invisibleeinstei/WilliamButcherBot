"""
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
from time import time

from pyrogram import filters
from pyrogram.types import CallbackQuery, ChatPermissions, Message

from wbb import BOT_ID, SUDOERS, app
from wbb.core.decorators.errors import capture_err
from wbb.core.keyboard import ikb
from wbb.utils.dbfunctions import (add_warn, get_warn, int_to_alpha,
                                   remove_warns, save_filter)
from wbb.utils.functions import (extract_user, extract_user_and_reason,
                                 time_converter)

__MODULE__ = "Admin"
__HELP__ = """/ban - ʙᴀɴ ᴀ ᴜꜱᴇʀ
/dban - ᴅᴇʟᴇᴛᴇ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴍᴇꜱꜱᴀɢᴇ ʙᴀɴɴɪɴɢ ɪᴛꜱ ꜱᴇɴᴅᴇʀ
/tban - ʙᴀɴ ᴀ ᴜꜱᴇʀ ꜰᴏʀ ꜱᴘᴇᴄɪꜰɪᴄ ᴛɪᴍᴇ
/unban - ᴜɴʙᴀɴ ᴀ ᴜꜱᴇʀ
/warn - ᴡᴀʀɴ ᴀ ᴜꜱᴇʀ
/dwarn - ᴅᴇʟᴇᴛᴇ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴍᴇꜱꜱᴀɢᴇ ᴡᴀʀɴɪɴɢ ɪᴛꜱ ꜱᴇɴᴅᴇʀ
/rmwarns - ʀᴇᴍᴏᴠᴇ ᴀʟʟ ᴡᴀʀɴɪɴɢ ᴏꜰ ᴀ ᴜꜱᴇʀ
/warns - ꜱʜᴏᴡ ᴡᴀʀɴɪɴɢ ᴏꜰ ᴀ ᴜꜱᴇʀ
/kick - ᴋɪᴄᴋ ᴀ ᴜꜱᴇʀ
/dkick - ᴅᴇʟᴇᴛᴇ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴍᴇꜱꜱᴀɢᴇ ᴋɪᴄᴋɪɴɢ ɪᴛꜱ ꜱᴇɴᴅᴇʀ
/purge - ᴘᴜʀɢᴇ ᴍᴇꜱꜱᴀɢᴇꜱ
/del - ᴅᴇʟᴇᴛᴇ ʀᴇᴘʟɪᴇᴅ ᴍᴇꜱꜱᴀɢᴇ
/promote - ᴘʀᴏᴍᴏᴛᴇ ᴀ ᴍᴇᴍʙᴇʀ
/fullpromote - ᴘʀᴏᴍᴏᴛᴇ ᴀ ᴍᴇᴍʙᴇʀ ᴡɪᴛʜ ᴀʟʟ ʀɪɢʜᴛꜱ
/demote - ᴅᴇᴍᴏᴛᴇ ᴀ ᴍᴇᴍʙᴇʀ
/pin - ᴘɪɴ ᴀ ᴍᴇꜱꜱᴀɢᴇ
/mute - ᴍᴜᴛᴇ ᴀ ᴜꜱᴇʀ
/tmute - ᴍᴜᴛᴇ ᴀ ᴜꜱᴇʀ ꜰᴏʀ ꜱᴘᴇᴄɪꜰɪᴄ ᴛɪᴍᴇ
/unmute - ᴜɴᴍᴜᴛᴇ ᴀ ᴜꜱᴇʀ
/ban_ghosts - ʙᴀɴ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ
/report | @admins | @admin - ʀᴇᴘᴏʀᴛ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀᴅᴍɪɴꜱ."""


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = await app.get_chat_member(chat_id, user_id)
    except Exception:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms


from wbb.core.decorators.permissions import adminsOnly

admins_in_chat = {}


async def list_admins(chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in app.iter_chat_members(
                chat_id, filter="administrators"
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


async def current_chat_permissions(chat_id):
    perms = []
    perm = (await app.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")

    return perms


# Purge Messages


@app.on_message(filters.command("purge") & ~filters.edited & ~filters.private)
@adminsOnly("can_delete_messages")
async def purgeFunc(_, message: Message):
    await message.delete()

    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to purge from.")

    chat_id = message.chat.id
    message_ids = []

    for message_id in range(
        message.reply_to_message.message_id,
        message.message_id,
    ):
        message_ids.append(message_id)

        # Max message deletion limit is 100
        if len(message_ids) == 100:
            await app.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,  # For both sides
            )

            # To delete more than 100 messages, start again
            message_ids = []

    # Delete if any messages left
    if len(message_ids) > 0:
        await app.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )


# Kick members


@app.on_message(
    filters.command(["kick", "dkick"]) & ~filters.edited & ~filters.private
)
@adminsOnly("can_restrict_members")
async def kickFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ.")
    if user_id == BOT_ID:
        return await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴍʏꜱᴇʟꜰ, ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ.😅🤦🏻"
        )
    if user_id in SUDOERS:
        return await message.reply_text("ʏᴏᴜ ᴡᴀɴɴᴀ ᴋɪᴄᴋ ᴛʜᴇ ᴇʟᴇᴠᴀᴛᴇᴅ ᴏɴᴇ?")
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴀɴ ᴀᴅᴍɪɴ, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇꜱ, ꜱᴏ ᴅᴏ ɪ.🙆🏻"
        )
    mention = (await app.get_users(user_id)).mention
    msg = f"""
**Kicked User:** {mention}
**Kicked By:** {message.from_user.mention if message.from_user else 'Anon'}
**Reason:** {reason or 'No Reason Provided.'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)


# Ban members


@app.on_message(
    filters.command(["ban", "dban", "tban"])
    & ~filters.edited
    & ~filters.private
)
@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ.")
    if user_id == BOT_ID:
        return await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴍʏꜱᴇʟꜰ, ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ.😅🤦🏻"
        )
    if user_id in SUDOERS:
        return await message.reply_text(
            "ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴀɴ ᴛʜᴇ ᴇʟᴇᴠᴀᴛᴇᴅ ᴏɴᴇ?, ʀᴇᴄᴏɴꜱɪᴅᴇʀ!"
        )
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴀɴ ᴀᴅᴍɪɴ, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇꜱ, ꜱᴏ ᴅᴏ ɪ.🙆🏻"
        )

    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )

    msg = (
        f"**Banned User:** {mention}\n"
        f"**Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if message.command[0] == "tban":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_ban = await time_converter(message, time_value)
        msg += f"**Banned For:** {time_value}\n"
        if temp_reason:
            msg += f"**Reason:** {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.ban_member(user_id, until_date=temp_ban)
                await message.reply_text(msg)
            else:
                await message.reply_text("You can't use more than 99")
        except AttributeError:
            pass
        return
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)


# Unban members


@app.on_message(filters.command("unban") & ~filters.edited & ~filters.private)
@adminsOnly("can_restrict_members")
async def unbanFunc(_, message: Message):
    # we don't need reasons for unban, also, we
    # don't need to get "text_mention" entity, because
    # normal users won't get text_mention if the the user
    # they want to unban is not in the group.
    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and message.reply_to_message:
        user = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(
            "ᴘʀᴏᴠɪᴅᴇ ᴀ ᴜꜱᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ'ꜱ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴜɴʙᴀɴ."
        )
    await message.chat.unban_member(user)
    umention = (await app.get_users(user)).mention
    await message.reply_text(f"Unbanned! {umention}")


# Delete messages


@app.on_message(filters.command("del") & ~filters.edited & ~filters.private)
@adminsOnly("can_delete_messages")
async def deleteFunc(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply To A Message To Delete It")
    await message.reply_to_message.delete()
    await message.delete()


# Promote Members


@app.on_message(
    filters.command(["promote", "fullpromote"])
    & ~filters.edited
    & ~filters.private
)
@adminsOnly("can_promote_members")
async def promoteFunc(_, message: Message):
    user_id = await extract_user(message)
    umention = (await app.get_users(user_id)).mention
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ.")
    bot = await app.get_chat_member(message.chat.id, BOT_ID)
    if user_id == BOT_ID:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ᴍʏꜱᴇʟꜰ.")
    if not bot.can_promote_members:
        return await message.reply_text("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ")
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id=user_id,
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=bot.can_pin_messages,
            can_promote_members=bot.can_promote_members,
            can_manage_chat=bot.can_manage_chat,
            can_manage_voice_chats=bot.can_manage_voice_chats,
        )
        return await message.reply_text(f"Fully Promoted! {umention}")

    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=bot.can_invite_users,
        can_delete_messages=bot.can_delete_messages,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=bot.can_manage_chat,
        can_manage_voice_chats=bot.can_manage_voice_chats,
    )
    await message.reply_text(f"Promoted! {umention}")


# Demote Member


@app.on_message(filters.command("demote") & ~filters.edited & ~filters.private)
@adminsOnly("can_promote_members")
async def demote(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ.")
    if user_id == BOT_ID:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴅᴇᴍᴏᴛᴇ ᴍʏꜱᴇʟꜰ.")
    if user_id in SUDOERS:
        return await message.reply_text(
            "ʏᴏᴜ ᴡᴀɴɴᴀ ᴅᴇᴍᴏᴛᴇ ᴛʜᴇ ᴇʟᴇᴠᴀᴛᴇᴅ ᴏɴᴇ?, ʀᴇᴄᴏɴꜱɪᴅᴇʀ!"
        )
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=False,
        can_delete_messages=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_voice_chats=False,
    )
    umention = (await app.get_users(user_id)).mention
    await message.reply_text(f"Demoted! {umention}")


# Pin Messages


@app.on_message(
    filters.command(["pin", "unpin"]) & ~filters.edited & ~filters.private
)
@adminsOnly("can_pin_messages")
async def pin(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴘɪɴ/ᴜɴᴘɪɴ ɪᴛ.📌")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await message.reply_text(
            f"**Unpinned [this]({r.link}) message.**",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await message.reply(
        f"**Pinned [this]({r.link}) message.**",
        disable_web_page_preview=True,
    )
    msg = "ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴘɪɴɴᴇᴅ ᴍᴇꜱꜱᴀɢᴇ: ~ " + f"[Check, {r.link}]"
    filter_ = dict(type="text", data=msg)
    await save_filter(message.chat.id, "~pinned", filter_)


# Mute members


@app.on_message(
    filters.command(["mute", "tmute"]) & ~filters.edited & ~filters.private
)
@adminsOnly("can_restrict_members")
async def mute(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ.")
    if user_id == BOT_ID:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴍᴜᴛᴇ ᴍʏꜱᴇʟꜰ.")
    if user_id in SUDOERS:
        return await message.reply_text(
            "ʏᴏᴜ ᴡᴀɴɴᴀ ᴍᴜᴛᴇ ᴛʜᴇ ᴇʟᴇᴠᴀᴛᴇᴅ ᴏɴᴇ?, ʀᴇᴄᴏɴꜱɪᴅᴇʀ!"
        )
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴍᴜᴛᴇ ᴀɴ ᴀᴅᴍɪɴ, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇꜱ, ꜱᴏ ᴅᴏ ɪ."
        )
    mention = (await app.get_users(user_id)).mention
    keyboard = ikb({"🚨   Unmute   🚨": f"unmute_{user_id}"})
    msg = (
        f"**Muted User:** {mention}\n"
        f"**Muted By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0] == "tmute":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_mute = await time_converter(message, time_value)
        msg += f"**Muted For:** {time_value}\n"
        if temp_reason:
            msg += f"**Reason:** {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.restrict_member(
                    user_id,
                    permissions=ChatPermissions(),
                    until_date=temp_mute,
                )
                await message.reply_text(msg, reply_markup=keyboard)
            else:
                await message.reply_text("You can't use more than 99")
        except AttributeError:
            pass
        return
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await message.reply_text(msg, reply_markup=keyboard)


# Unmute members


@app.on_message(filters.command("unmute") & ~filters.edited & ~filters.private)
@adminsOnly("can_restrict_members")
async def unmute(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ.")
    await message.chat.unban_member(user_id)
    umention = (await app.get_users(user_id)).mention
    await message.reply_text(f"Unmuted! {umention}")


# Ban deleted accounts


@app.on_message(filters.command("ban_ghosts") & ~filters.private)
@adminsOnly("can_restrict_members")
async def ban_deleted_accounts(_, message: Message):
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    m = await message.reply("Finding ghosts...")

    async for i in app.iter_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                await message.chat.ban_member(deleted_user)
            except Exception:
                pass
            banned_users += 1
        await m.edit(f"ʙᴀɴɴᴇᴅ {banned_users} ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ")
    else:
        await m.edit("ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ")


@app.on_message(
    filters.command(["warn", "dwarn"]) & ~filters.edited & ~filters.private
)
@adminsOnly("can_restrict_members")
async def warn_user(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    chat_id = message.chat.id
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ.")
    if user_id == BOT_ID:
        return await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴍʏꜱᴇʟꜰ, ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ."
        )
    if user_id in SUDOERS:
        return await message.reply_text(
            "ʏᴏᴜ ᴡᴀɴɴᴀ ᴡᴀʀɴ ᴛʜᴇ ᴇʟᴇᴠᴀᴛᴇᴅ ᴏɴᴇ?, ʀᴇᴄᴏɴꜱɪᴅᴇʀ!"
        )
    if user_id in (await list_admins(chat_id)):
        return await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴀɴ ᴀᴅᴍɪɴ, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇꜱ, ꜱᴏ ᴅᴏ ɪ."
        )
    user, warns = await asyncio.gather(
        app.get_users(user_id),
        get_warn(chat_id, await int_to_alpha(user_id)),
    )
    mention = user.mention
    keyboard = ikb({"🚨  Remove Warn  🚨": f"unwarn_{user_id}"})
    if warns:
        warns = warns["warns"]
    else:
        warns = 0
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if warns >= 2:
        await message.chat.ban_member(user_id)
        await message.reply_text(
            f"Number of warns of {mention} exceeded, BANNED!"
        )
        await remove_warns(chat_id, await int_to_alpha(user_id))
    else:
        warn = {"warns": warns + 1}
        msg = f"""
**Warned User:** {mention}
**Warned By:** {message.from_user.mention if message.from_user else 'Anon'}
**Reason:** {reason or 'No Reason Provided.'}
**Warns:** {warns + 1}/3"""
        await message.reply_text(msg, reply_markup=keyboard)
        await add_warn(chat_id, await int_to_alpha(user_id), warn)


@app.on_callback_query(filters.regex("unwarn_"))
async def remove_warning(_, cq: CallbackQuery):
    from_user = cq.from_user
    chat_id = cq.message.chat.id
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await cq.answer(
            "You don't have enough permissions to perform this action.\n"
            + f"Permission needed: {permission}",
            show_alert=True,
        )
    user_id = cq.data.split("_")[1]
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if not warns or warns == 0:
        return await cq.answer("User has no warnings.")
    warn = {"warns": warns - 1}
    await add_warn(chat_id, await int_to_alpha(user_id), warn)
    text = cq.message.text.markdown
    text = f"~~{text}~~\n\n"
    text += f"__Warn removed by {from_user.mention}__"
    await cq.message.edit(text)


# Rmwarns


@app.on_message(
    filters.command("rmwarns") & ~filters.edited & ~filters.private
)
@adminsOnly("can_restrict_members")
async def remove_warnings(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀ ᴜꜱᴇʀ'ꜱ ᴡᴀʀɴɪɴɢꜱ."
        )
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    chat_id = message.chat.id
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if warns == 0 or not warns:
        await message.reply_text(f"{mention} have no warnings.")
    else:
        await remove_warns(chat_id, await int_to_alpha(user_id))
        await message.reply_text(f"Removed warnings of {mention}.")


# Warns


@app.on_message(filters.command("warns") & ~filters.edited & ~filters.private)
@capture_err
async def check_warns(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ.")
    warns = await get_warn(message.chat.id, await int_to_alpha(user_id))
    mention = (await app.get_users(user_id)).mention
    if warns:
        warns = warns["warns"]
    else:
        return await message.reply_text(f"{mention} has no warnings.")
    return await message.reply_text(f"{mention} has {warns}/3 warnings.")


# Report


@app.on_message(
    (
        filters.command("report")
        | filters.command(["admins", "admin"], prefixes="@")
    )
    & ~filters.edited
    & ~filters.private
)
@capture_err
async def report_user(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʀᴇᴘᴏʀᴛ ᴛʜᴀᴛ ᴜꜱᴇʀ."
        )

    if message.reply_to_message.from_user.id == message.from_user.id:
        return await message.reply_text("ᴡʜʏ ᴀʀᴇ ʏᴏᴜ ʀᴇᴘᴏʀᴛɪɴɢ ʏᴏᴜʀꜱᴇʟꜰ ?")

    list_of_admins = await list_admins(message.chat.id)
    if message.reply_to_message.from_user.id in list_of_admins:
        return await message.reply_text(
            "ᴅᴏ ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴀᴛ ᴛʜᴇ ᴜꜱᴇʀ ʏᴏᴜ ᴀʀᴇ ʀᴇᴘʟʏɪɴɢ ɪꜱ ᴀɴ ᴀᴅᴍɪɴ ?"
        )

    user_mention = message.reply_to_message.from_user.mention
    text = f"Reported {user_mention} to admins!"
    admin_data = await app.get_chat_members(
        chat_id=message.chat.id, filter="administrators"
    )  # will it giv floods ?
    for admin in admin_data:
        if admin.user.is_bot or admin.user.is_deleted:
            # return bots or deleted admins
            continue
        text += f"[\u2063](tg://user?id={admin.user.id})"

    await message.reply_to_message.reply_text(text)
