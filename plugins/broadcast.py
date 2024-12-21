import datetime, time, os, asyncio, logging 
from pyrogram import Client, filters, enums
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram.types import Message, InlineKeyboardButton
from database.users_chats_db import db
from info import ADMINS
from utils import broadcast_messages
import asyncio
        
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def speed_verupikkals(bot, message):
    if len(message.command) == 1:
        matrix = 0  # No matrix value provided, skip no users
    else:
        try:
            matrix = int(message.text.split(None, 1)[1])  # Extract matrix value
        except ValueError:
            await message.reply("Invalid matrix value. Please enter a number.")
            return  # Exit function if matrix value is invalid
    start_time = time.time()
    b_msg = message.reply_to_message
    sts = await message.reply("processing...")
    users = await db.get_all_users()
    users_list = await users.to_list(None)  
    total_users = len(users_list)    
    users = await db.get_all_users() 
    # Skip specified number of users
    skipped_count = 0
    success = 0
    failed = 0
    async for user in users:  # Iterate directly over cursor
        if skipped_count < matrix:
            skipped_count += 1             
        else:# Skip users until reaching the desired matrix value
            try:
                await b_msg.copy(chat_id=int(user['id']))
                success += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await b_msg.copy(chat_id=int(user['id']))
            except InputUserDeactivated:
                await db.delete_user(int(user['id']))
                failed += 1
            except UserIsBlocked:
                await db.delete_user(int(user['id']))
                failed += 1
            except Exception as e:                
                failed += 1

        process = success + failed

        if process % 500 == 1:
            elapsed_time = datetime.timedelta(seconds=int(time.time() - start_time))
            await sts.edit(f"Progress: {process+matrix}/{total_users}\nSuccess: {success}\nFailed: {failed}\nElapsed Time: {elapsed_time}")

    # No need for separate start_time variable as loop starts here
    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts.edit(f"Completed\nTotal : {total_users}\nSuccess : {success}\nSkipped : {skipped_count}\nFailed : {failed}\nTime Taken : {time_taken}")

@Client.on_message(filters.command("grp_broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_group(bot, message):
    groups = await db.get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(text='🚀')
    start_time = time.time()
    total_groups = await db.total_chat_count()
    done = 0
    failed = ""
    success = 0
    deleted = 0
    async for group in groups:
        pti, sh, ex = await broadcast_messages_group(int(group['id']), b_msg)
        if pti == True:
            if sh == "Succes":
                success += 1
        elif pti == False:
            if sh == "deleted":
                deleted+=1 
                failed += ex 
                try:
                    await bot.leave_chat(int(group['id']))
                except Exception as e:
                    print(f"{e} > {group['id']}")  
        done += 1
        if not done % 20:
            await sts.edit(f"𝖨𝗇 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌.\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌: {total_groups}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_groups}\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: {success}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.delete()
    try:
        await message.reply_text(f"𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽.\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝖨𝗇: {time_taken} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌.\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌: {total_groups}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_groups}\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: {success}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}\n\n𝖱𝖾𝖺𝗌𝗈𝗇:- {failed}")
    except MessageTooLong:
        with open('reason.txt', 'w+') as outfile:
            outfile.write(failed)
        await message.reply_document('reason.txt', caption=f"𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽.\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝖨𝗇: {time_taken} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌.\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌: {total_groups}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_groups}\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: {success}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}")
        os.remove("reason.txt")