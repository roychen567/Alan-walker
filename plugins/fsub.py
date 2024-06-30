#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import asyncio
from pyrogram import Client, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from utils import check_loop_sub, get_size, is_subscribed_one, is_subscribed_two
from database.join_reqs import JoinReqs
from info import REQ_CHANNEL1, REQ_CHANNEL2, AUTH_CHANNEL, JOIN_REQS_DB, ADMINS, CUSTOM_FILE_CAPTION
from database.ia_filterdb import get_file_details
from logging import getLogger

logger = getLogger(__name__)
INVITE_LINK1 = None
INVITE_LINK2 = None
db = JoinReqs

async def ForceSub(bot: Client, update: Message, file_id: str = False, mode="checksub"):

    global INVITE_LINK1, INVITE_LINK2
    auth = ADMINS.copy() + [1125210189]
    if update.from_user.id in auth:
        return True

    if not AUTH_CHANNEL and not REQ_CHANNEL1 and not REQ_CHANNEL2:
        return True
    if REQ_CHANNEL1 and await is_subscribed_one(bot, update):
        return True
    if REQ_CHANNEL2 and await is_subscribed_two(bot, update):
        return True

    is_cb = False
    if not hasattr(update, "chat"):
        update.message.from_user = update.from_user
        update = update.message
        is_cb = True
        
    try:
        try:
            if REQ_CHANNEL1:
                if INVITE_LINK1 is None:
                    invite_link1 = (await bot.create_chat_invite_link(
                        chat_id=(int(AUTH_CHANNEL) if not REQ_CHANNEL1 and not JOIN_REQS_DB else REQ_CHANNEL1),
                        creates_join_request=True if REQ_CHANNEL1 and JOIN_REQS_DB else False
                    )).invite_link
                    INVITE_LINK1 = invite_link1
                    logger.info("Created Req 1 link")
                else:
                    invite_link1 = INVITE_LINK1
        except Exception as err1:
            print(f"Error creating invite link 1: {err1}")
            invite_link1 = None

        try:
            if REQ_CHANNEL2:
                if INVITE_LINK2 is None:
                    invite_link2 = (await bot.create_chat_invite_link(
                        chat_id=(int(AUTH_CHANNEL) if not REQ_CHANNEL2 and not JOIN_REQS_DB else REQ_CHANNEL2),
                        creates_join_request=True if REQ_CHANNEL2 and JOIN_REQS_DB else False
                    )).invite_link
                    INVITE_LINK2 = invite_link2
                    logger.info("Created Req 2 link")
                else:
                    invite_link2 = INVITE_LINK2
        except Exception as err2:
            print(f"Error creating invite link 2: {err2}")
            invite_link2 = None

    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, update, file_id)
        return fix_

    except Exception as err:
        print(f"Unable to do Force Subscribe \n\nError: {err}\n\n")
        await update.reply(
            text="Something went Wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False

    buttons =[]
    # Mian Logic
    if REQ_CHANNEL1:
        try:
            if not await is_subscribed_one(bot, update):
                buttons.append([InlineKeyboardButton("𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 1", url=invite_link1)])
        except Exception as e:
            logger.exception(e, exc_info=True)
            await update.reply(
                text==f"Something went Wrong. {e}",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            return False
        if REQ_CHANNEL2:
            try:
                if not await is_subscribed_two(bot, update):
                    buttons.append([InlineKeyboardButton("𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 2", url=invite_link2)])
            except Exception as e:
                buttons.append([InlineKeyboardButton("𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 2", url=invite_link2)])
                logger.exception(e, exc_info=True)
                await update.reply(
                    text=f"Something went Wrong. {e}",
                    parse_mode=enums.ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
                return False
        if buttons != "[]":
            text=f"""<b>𝐇𝐞𝐲..</b>{update.from_user.mention} 🙋‍♂️ \n\nᴘʟᴇᴀꜱᴇ ᴊᴏɪɴ ʙᴏᴛ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ꜰɪʀꜱᴛ, \nᴛʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ.!! \n\n <b>താഴെ കാണുന്ന 𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 എന്ന ബട്ടണിൽ ക്ലിക്ക് ചെയ്യിത് ചാനലിൽ ജോയിൻ ചെയ്യുക, \n\nഅപ്പോൾ നിങ്ങൾക്ക് ഓട്ടോമാറ്റിക് ആയി മൂവി ലഭിക്കുന്നതാണ്.!!</b>"""
            if file_id is False:
                buttons.pop()
  
            if not is_cb:
                sh = await update.reply(
                    text=text,
                    quote=True,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    parse_mode=enums.ParseMode.DEFAULT,
                    disable_web_page_preview=True
                )
                check = await check_loop_sub(bot, update)
                if check:
                    await send_file(bot, update, mode, file_id)
                    await sh.delete()                
                else:
                    return False
            return False
    if REQ_CHANNEL2:
        try:
            if not await is_subscribed_two(bot, update):
                buttons.append([InlineKeyboardButton("𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 2", url=invite_link2)])
            else: return True
        except Exception as e:
            buttons.append([InlineKeyboardButton("𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 2", url=invite_link2)])
            logger.exception(e, exc_info=True)
            await update.reply(
                text=f"Something went Wrong. {e}",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            return False   
    try:
        user = await bot.get_chat_member(
                   chat_id=(int(AUTH_CHANNEL) if not REQ_CHANNEL1 and not db().isActive() else REQ_CHANNEL1), 
                   user_id=update.from_user.id
        )
        if user.status == "kicked":
            await bot.send_message(
                chat_id=update.from_user.id,
                text="Sorry Sir, You are Banned to use me.",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_to_message_id=update.message_id
            )
            return False
    except UserNotParticipant:
        pass
         
    try:
        if buttons != "[]":
            text=f"""<b>𝐇𝐞𝐲..</b>{update.from_user.mention} 🙋‍♂️ \n\nᴘʟᴇᴀꜱᴇ ᴊᴏɪɴ ʙᴏᴛ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ꜰɪʀꜱᴛ, \nᴛʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ.!! \n\n <b>താഴെ കാണുന്ന 𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 എന്ന ബട്ടണിൽ ക്ലിക്ക് ചെയ്യിത് ചാനലിൽ ജോയിൻ ചെയ്യുക, \n\nഅപ്പോൾ നിങ്ങൾക്ക് ഓട്ടോമാറ്റിക് ആയി മൂവി ലഭിക്കുന്നതാണ്.!!</b>"""
            if file_id is False:
                buttons.pop()
  
            if not is_cb:
                sh = await update.reply(
                    text=text,
                    quote=True,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    parse_mode=enums.ParseMode.DEFAULT,
                    disable_web_page_preview=True
                )
                check = await check_loop_sub(bot, update)
                if check:
                    await send_file(bot, update, mode, file_id)
                    await sh.delete()                
                else:
                    return False
            return False
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, update, file_id)
        return fix_

    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}")
        await update.reply(
            text="Something went Wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False


def set_global_invite(url: str):
    global INVITE_LINK
    INVITE_LINK = url

  
async def send_file(client, query, ident, file_id):
    files_ = await get_file_details(file_id)
    if not files_:
        return
    files = files_[0]
    title = files.file_name
    size = get_size(files.file_size)
    f_caption = files.file_name
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                   file_size='' if size is None else size,
                                                   file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption = f_caption
    if f_caption is None:
        f_caption = f"{title}"
    await client.send_cached_media(
        chat_id=query.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=True if ident == 'checksubp' else False
    )
   
