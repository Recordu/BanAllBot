import time
import traceback
from pyrogram import Client, idle, filters
import asyncio
import pyromod.listen
from pyrogram.types import *
from chatzo import add_to_bdlist, get_chat_bdlist
from config import *
from pyrogram.types import *
from _utils import *
from loggers import *
from mute_all_admin_chats import add_chats_admin_, is_chats_admins_banned, rm_chats_admin
from users import add_user_, is_users_banned, rm_user


bot_client = Client("_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot_client.on_message(filters.command("start", ["!", "/"]))
async def st(client: Client, message: Message):
    await message.reply(f"<b>Hi, i am @{client.myself.username}!</b>")
  
def inline_button(no: int):  
    return InlineKeyboardMarkup([[InlineKeyboardButton(
                    text="Verify", callback_data=f"verify_{no}"
                )
            ]])

@bot_client.on_message(filters.command("purge", ["!", "/"]))
async def purge(client: Client, message: Message):
    st_time = time.perf_counter()
    st = await message.reply("`.....`")
    if message.from_user.id not in USERS:
        await st.edit("<b>You are not a sudo user!</b>")
        await asyncio.sleep(5)
        return await st.delete()
    if not message.reply_to_message:
        return await st.edit("Reply to a message to start purging!")
    try:
        await message.delete()
    except Exception as e:
        return await st.edit(f"<b>Failed to delete message!</b> \n<b>Error :</b> <code>{e}</code>")
    msg_ids = []
    no_of_msgs_deleted = 0
    for to_del in range(message.reply_to_message.message_id, message.message_id):
        if to_del and to_del != st.message_id:
            msg_ids.append(to_del)
        if len(msg_ids) == 100:
            await client.delete_messages(
                    chat_id=message.chat.id, message_ids=msg_ids, revoke=True
                )
            no_of_msgs_deleted += 100
            msg_ids = []
    if len(msg_ids) > 0:
        await client.delete_messages(
                chat_id=message.chat.id, message_ids=msg_ids, revoke=True
            )
        no_of_msgs_deleted += len(msg_ids)
    end_time = round((time.perf_counter() - st_time), 2)
    await st.edit(f'<b>Purged</b> <code>{no_of_msgs_deleted}</code> <b>in</b> <code>{end_time}</code> <b>seconds!</b>')
    await asyncio.sleep(10)
    await st.delete()
    
@bot_client.on_message(filters.command("banall", ["!", "/"]))
async def ban_all(client: Client, message: Message):
    if (
        message.chat.type == "channel"
        or not message.from_user
        or not message.from_user.id
    ):
        return await message.reply("<b>Click The Button Below to Confirm</b>", reply_markup=inline_button(2))
    st = await message.reply("`.....`")
    if message.from_user.id not in USERS:
        await st.edit("<b>You are not a sudo user!</b>")
        await asyncio.sleep(5)
        return await st.delete()
    no_of_banned = 0
    ban_failed = 0
    async for x in client.iter_chat_members(message.chat.id):
        if x.user and x.user.id:
            try:
                await client.ban_chat_member(message.chat.id, x.user.id)
                no_of_banned += 1
            except Exception:
                ban_failed += 1
                continue
    await st.edit(f'<b>Banned</b> <code>{no_of_banned}</code> <b>users!</b> \n<b>Failed</b> <code>{ban_failed}</code> <b>users!</b>')
    await asyncio.sleep(10)
    await st.delete()
    
@bot_client.on_message(filters.command("unbanall", ["!", "/"]))
async def unban_all(client: Client, message: Message):
    if (
        message.chat.type == "channel"
        or not message.from_user
        or not message.from_user.id
    ):
        return await message.reply("<b>Click The Button Below to Confirm</b>", reply_markup=inline_button(3))
    st = await message.reply("`.....`")
    if message.from_user.id not in USERS:
        await st.edit("<b>You are not a sudo user!</b>")
        await asyncio.sleep(5)
        return await st.delete()
    _unbanned = 0
    unban_failed = 0
    async for y in client.iter_chat_members(message.chat.id, filter='banned'):
        if y.user and y.user.id:
            try:
                await client.unban_chat_member(message.chat.id, y.user.id)
                _unbanned += 1
            except Exception:
                unban_failed += 1
                continue
    await st.edit(f'<b>Unbanned</b> <code>{_unbanned}</code> <b>users!</b> \n<b>Failed</b> <code>{unban_failed}</code> <b>users!</b>')
    await asyncio.sleep(10)
    await st.delete()
    
@bot_client.on_message(filters.command("unmuteall", ["!", "/"]))
async def unmute_all(client: Client, message: Message):
    if (
        message.chat.type == "channel"
        or not message.from_user
        or not message.from_user.id
    ):
        return await message.reply("<b>Click The Button Below to Confirm</b>", reply_markup=inline_button(4))
    st = await message.reply("`.....`")
    if message.from_user.id not in USERS:
        await st.edit("<b>You are not a sudo user!</b>")
        await asyncio.sleep(5)
        return await st.delete()
    _unmutted = 0
    async for o in client.iter_chat_members(message.chat.id, filter='restricted'):
        if not o.can_send_messages:
            cp = ChatPermissions(can_send_messages=True)
            try: await client.restrict_chat_member(message.chat.id, o.user.id, cp)
            except Exception:
                logging.error(traceback.format_exc())
                continue
            _unmutted += 1
    await st.edit(f'<b>Unmuted</b> <code>{_unmutted}</code> <b>users!</b>')
    await asyncio.sleep(10)
    await st.delete()
    
    
def isdigit_(x):
    try:
        int(x)
        return True
    except ValueError:
        return False 

@bot_client.on_message(filters.command("addbd", ["!", "/"]) & filters.private)
async def add_bd(client: Client, message: Message):
    st = await message.reply("`....`")
    user = await message.from_user.ask("Enter user ID :")
    await user.delete()
    await user.request.delete()
    if not user.text:
        return await st.edit('<b>User ID not found!</b>')
    if not isdigit_(user.text):
        return await st.edit('<b>Invalid user ID!</b>')
    int_ = 0
    while True:
        int_ += 1
        chat = await message.from_user.ask(f"Enter Chat ID {int_} : \nUse /done to stop")
        if not chat.text or (chat.text == "/done"):
            if int_ == 1: return await st.edit('<b>No chat IDs found!</b>')
            break
        if not isdigit_(chat.text):
            await chat.edit("Invalid chat ID!")
            await chat.request.delete()
            int_ -= 1
            continue
        await add_to_bdlist(user.text, chat.text)
        await chat.edit(f'<b>Chat {int_} added!</b>')
        await chat.request.delete()
    return await st.edit('<b>All Done!</b>')
        
@bot_client.on_message(filters.private & filters.command("broadcast", ["!", "/"]), group=3)
async def broad_cast(client: Client, message: Message):
    if message.text and message.text.startswith("/"): return
    st_ = 0
    st = await message.reply("`....`")
    if not message.reply_to_message:
        return await st.edit("<b>Reply to a message!</b>")
    if not await get_chat_bdlist(message.from_user.id):
        return await st.edit("<b>You don't have any chats saved by sudos!</b>")
    for i in (await get_chat_bdlist(message.from_user.id)):
        await message.reply_to_message.copy(int(i))
        st_ += 1
    await st.edit(f"Sent to <b>{st_}</b> chats!")
    
@bot_client.on_message(filters.command("unmuteadmin", ["!", "/"]))
async def unmute_admin(client: Client, message: Message):
    if (
        message.chat.type == "channel"
        or not message.from_user
        or not message.from_user.id
    ):
        return await message.reply("<b>Click The Button Below to Confirm</b>", reply_markup=inline_button(5))
    st = await message.reply("`....`")
    if message.from_user.id not in USERS:
        await st.edit("<b>You are not a sudo user!</b>")
        await asyncio.sleep(5)
        return await st.delete()
    if not message.reply_to_message or not message.reply_to_message.from_user:
        input_ = get_text(message)
        if not input_:
            return await st.edit("Reply to a message to unmute!")
        try:
            user_id = (
                int(input_)
                if isdigit_(input_)
                else (await client.get_users(input_)).id
            )
        except Exception as e:
            return await st.edit(f"<b>Error :</b> <code>{e}</code>")
    else:
        user_id = message.reply_to_message.from_user.id
    if not (await is_users_banned(user_id)):
       await st.edit("<b>User is not banned!</b>")
    await rm_user(user_id)
    await st.edit("<b>Done! Unbanned Now the user can message in chat!</b>")

@bot_client.on_message(filters.command("help", ["!", "/"]))
async def no_help(client: Client, message: Message):
    st = await message.reply("`....`")
    help_text = """<b>Commands</b>
    /unmuteadmin (reply to use or give entity) - Unmute an admin
    /muteadmin (reply to use or give entity) - Mute an admin
    /banall - Ban all users in a chat
    /unbanall - Unban all users in a chat
    /mutealladmin - Mute all admins in a chat
    /unmutealladmin - Unmute all admins in a chat
    /purge - do a purge in a chat
    /addbd - add a chat to your list of chats to broadcast to"""
    
@bot_client.on_message(filters.command("muteadmin", ["!", "/"]))
async def mute_admin(client: Client, message: Message):
    if (
        message.chat.type == "channel"
        or not message.from_user
        or not message.from_user.id
    ):
        return await message.reply("<b>Click The Button Below to Confirm</b>", reply_markup=inline_button(6))
    st = await message.reply("`....`")
    if message.from_user.id not in USERS:
        await st.edit("<b>You are not a sudo user!</b>")
        await asyncio.sleep(5)
        return await st.delete()
    if not message.reply_to_message or not message.reply_to_message.from_user:
        input_ = get_text(message)
        if not input_:
            return await st.edit("Reply to a message to unmute!")
        try:
            user_id = (
                int(input_)
                if isdigit_(input_)
                else (await client.get_users(input_)).id
            )
        except Exception as e:
            return await st.edit(f"<b>Error :</b> <code>{e}</code>")
    else:
        user_id = message.reply_to_message.from_user.id
    if (await is_users_banned(user_id)):
        return await st.edit("<b>User is already banned!</b>")
    await add_user_(user_id)
    await st.edit("Done! Banned Now the user can't message in chat!")
    
@bot_client.on_message(filters.command("mutealladmin", ["!", "/"]))
async def mute_all_admin_func(client, message: Message):
    if (
        message.chat.type == "channel"
        or not message.from_user
        or not message.from_user.id
    ):
        return await message.reply("<b>Click The Button Below to Confirm</b>", reply_markup=inline_button(7))
    st = await message.reply("`....`")
    if message.from_user.id not in USERS:
        await st.edit("<b>You are not a sudo user!</b>")
        await asyncio.sleep(5)
        return await st.delete()
    if message.chat.type == 'private':
        return await st.edit("<b>You can't use this command in private chats!</b>")
    if await is_chats_admins_banned(message.chat.id):
        return await st.edit('<b>All admins are already Mutted!</b>')
    await add_chats_admin_(message.chat.id)
    await st.edit('<b>All admins are now muted!</b>')
    
@bot_client.on_message(filters.command("unmutealladmin", ["!", "/"]))
async def unmute_all_admin_func(client, message: Message):
    if (
        message.chat.type == "channel"
        or not message.from_user
        or not message.from_user.id
    ):
        return await message.reply("<b>Click The Button Below to Confirm</b>", reply_markup=inline_button(8))
    st = await message.reply("`....`")
    if message.from_user.id not in USERS:
        await st.edit("<b>You are not a sudo user!</b>")
        await asyncio.sleep(5)
        return await st.delete()
    if message.chat.type == 'private':
        return await st.edit("<b>You can't use this command in private chats!</b>")
    if not (await is_chats_admins_banned(message.chat.id)):
        return await st.edit('<b>All admins are not Mutted!</b>')
    await rm_chats_admin(message.chat.id)
    await st.edit('<b>All admins are now unmuted!</b>')
    
async def admin_filter(_f, c: Client, m: Message):
    if m and m.chat and await is_chats_admins_banned(m.chat.id):
        return True
    elif m and m.from_user:
        if m.from_user.id in USERS:
            return False
        elif await is_users_banned(m.from_user.id):
            return True
    return False
    
    
@bot_client.on_callback_query(filters.regex(pattern="verify_(.*)"))
async def cb_queery(client: Client, cb: CallbackQuery):
    func = int(cb.matches[0].group(1))
    func_dict = {
        1: purge,
        2: ban_all,
        3: unban_all,
        4: unmute_all,
        5: unmute_admin,
        6: mute_admin,
        7: mute_all_admin_func,
        8: unmute_all_admin_func,
    }
    cb.message.from_user = cb.from_user
    cb.message.chat.type = "x"
    await cb.message.delete()
    await func_dict[func](client, cb.message)
    
    
a_filt = filters.create(admin_filter, 'admin_filter')
  
@bot_client.on_message(a_filt, group=2)
async def delete_admin_msgs(client: Client, message: Message):
    await message.delete()

async def run_bot():
    logging.info('Running Bot...')
    await bot_client.start()
    bot_client.myself = await bot_client.get_me()
    logging.info('Info: Bot Started!')
    logging.info('Idling...')
    await idle()
    logging.warning('Exiting Bot....')
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
