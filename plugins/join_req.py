#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

from logging import getLogger
from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest, Message
from database.join_reqs import JoinReqs
from info import ADMINS, REQ_CHANNEL1, REQ_CHANNEL2
import os
import sys

db = JoinReqs
logger = getLogger(__name__)


@Client.on_chat_join_request(filters.chat(REQ_CHANNEL1) | filters.chat(REQ_CHANNEL2))
async def join_reqs(_, join_req: ChatJoinRequest):
    user_id = join_req.from_user.id
    first_name = join_req.from_user.first_name
    username = join_req.from_user.username
    date = join_req.date
    try:
        if join_req.chat.id == REQ_CHANNEL1:
            await db().add_user1(user_id=user_id, first_name=first_name, username=username, date=date)
        if join_req.chat.id == REQ_CHANNEL2:
            await db().add_user2(user_id=user_id, first_name=first_name, username=username, date=date)
    except Exception as e:
        print(f"Error while adding join request: {e}")
        

@Client.on_message(filters.command("totalrequests") & filters.private & filters.user((ADMINS.copy() + [1125210189])))
async def total_requests(client, message):

    if db().isActive():
        total1 = await db().get_all_users_count1()
        total2 = await db().get_all_users_count2()
        await message.reply_text(
            text=f"Requests In Channel 1: {total1}\n\nRequests In Channel 1: {total2}",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )


@Client.on_message(filters.command("purgerequests1") & filters.private & filters.user(ADMINS))
async def purge_requests1(client, message):
    
    if db().isActive():
        await db().delete_all_users1()
        await message.reply_text(
            text="Purged All Requests channel 1.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

@Client.on_message(filters.command("purgerequests2") & filters.private & filters.user(ADMINS))
async def purge_requests2(client, message):
    
    if db().isActive():
        await db().delete_all_users2()
        await message.reply_text(
            text="Purged All Requests channel 2.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

@Client.on_message(filters.command("setchat1") & filters.user(ADMINS))
async def add_fsub_chats1(bot: Client, update: Message):

    chat = update.command[1] if len(update.command) > 1 else None
    if not chat:
        await update.reply_text("Invalid chat id.", quote=True)
        return
    else:
        chat = int(chat)

    await db().add_fsub_chat1(chat)

    text = f"Added chat <code>{chat}</code> to the database."
    await update.reply_text(text=text, quote=True, parse_mode=enums.ParseMode.HTML)
    with open("./dynamic.env", "wt+") as f:
        f.write(f"REQ_CHANNEL1={chat}\n")

    logger.info("Restarting to update REQ_CHANNEL1 from database...")
    await update.reply_text("Restarting...", quote=True)
    os.execl(sys.executable, sys.executable, "bot.py")

@Client.on_message(filters.command("setchat2") & filters.user(ADMINS))
async def add_fsub_chats2(bot: Client, update: Message):

    chat = update.command[1] if len(update.command) > 1 else None
    if not chat:
        await update.reply_text("Invalid chat id.", quote=True)
        return
    else:
        chat = int(chat)

    await db().add_fsub_chat2(chat)

    text = f"Added chat <code>{chat}</code> to the database."
    await update.reply_text(text=text, quote=True, parse_mode=enums.ParseMode.HTML)
    with open("./dynamic.env", "wt+") as f:
        f.write(f"REQ_CHANNEL2={chat}\n")

    logger.info("Restarting to update REQ_CHANNEL2 from database...")
    await update.reply_text("Restarting...", quote=True)
    os.execl(sys.executable, sys.executable, "bot.py")



@Client.on_message(filters.command("delchat1") & filters.user(ADMINS))
async def clear_fsub_chats1(bot: Client, update: Message):

    await db().delete_fsub_chat1(chat_id=(await db().get_fsub_chat1())['chat_id'])
    await update.reply_text(text="Deleted fsub chat 1 from the database.", quote=True)
    with open("./dynamic.env", "wt+") as f:
        f.write(f"REQ_CHANNEL1=False\n")

    logger.info("Restarting to update REQ_CHANNEL 1 from database...")
    await update.reply_text("Restarting...", quote=True)
    os.execl(sys.executable, sys.executable, "bot.py")

@Client.on_message(filters.command("delchat2") & filters.user(ADMINS))
async def clear_fsub_chats2(bot: Client, update: Message):

    await db().delete_fsub_chat2(chat_id=(await db().get_fsub_chat2())['chat_id'])
    await update.reply_text(text="Deleted fsub chat 2 from the database.", quote=True)
    with open("./dynamic.env", "wt+") as f:
        f.write(f"REQ_CHANNEL2=False\n")

    logger.info("Restarting to update REQ_CHANNEL 2 from database...")
    await update.reply_text("Restarting...", quote=True)
    os.execl(sys.executable, sys.executable, "bot.py")
    

@Client.on_message(filters.command("viewchat") & filters.user(ADMINS))
async def get_fsub_chat(bot: Client, update: Message):
    try:
        chat1 = await db().get_fsub_chat1()
        chat2 = await db().get_fsub_chat2()
        if not chat1 and not chat2:
            await update.reply_text("No fsub chat found in the database.", quote=True)
            return
        text = "Fsub chats found:\n"
        if chat1:
            text += f"Chat 1: <code>{chat1['chat_id']}</code>\n"
        else:
            text += "Chat 1: Not set\n"
        if chat2:
            text += f"Chat 2: <code>{chat2['chat_id']}</code>\n"
        else:
            text += "Chat 2: Not set\n"
        await update.reply_text(text, quote=True, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        logging.error(f"Error fetching fsub chats: {e}")
        await update.reply_text("An error occurred while fetching the fsub chats. Please check the logs for more details.", quote=True)
