import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove 
from pyrogram import __version__ as pyrover
from typing import Dict, List, Union
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient

import time
import os
import threading
import asyncio



bot_token = os.environ.get("TOKEN", "5893575537:AAFNhlIFWpdwLPTzGd8QQxf1gILkdGrB8P8")
api_hash = os.environ.get("HASH", "f97624509b56289bfa5cff538b53bf4e") 
api_id = os.environ.get("ID", "29913370")
ss = os.environ.get("STRING", "BQAgDB0ZDpIyzGOFtRPECh02JdRhEhhW0fVMaq_OoIeq06SeKlaOot-AhjWcCrjc9xJQt_SaE2d12b-fj6_uFwbsVm_5w5Oc9eyl6m8twi1ZfzHiw1OjiFsYXh3Y6U9Kvoi545tbANl-nkUvgpz4Vvo-OjdMSzLO9aR2_tiQRGYmTMrt1fsyzcsWPPE271pGg0vANNF65wD3MeQlRr_ifjfTCXEyEhYMf3dCmOxv9wQeoXNfRJs6qnggy1KWnT8vL5DUpaXiuPlwPxe-hGPWwlu15B0TdwaD_u8eO0x2f3yrgPhmJGRYgF0XyvgiqtaNsOzc2FFO6Eu9FDn9cKvysaThAAAAAXFsFBMA")
bot = Client("mybot",api_id=api_id,api_hash=api_hash,bot_token=bot_token)
acc = Client("myacc",api_id=api_id,api_hash=api_hash,session_string=ss)


OWNER = 2089102006
MONGO = "mongodb+srv://safe:safe@cluster0.ijsgkme.mongodb.net/?retryWrites=true&w=majority"
_mongo_async_ = _mongo_client_(MONGO)
_mongo_sync_ = MongoClient(MONGO)
mongodb = _mongo_async_.twsl
pymongodb = _mongo_sync_.twsl
admins = [
          [
‎             ("الاحصائيات"),
‎             ("اذاعه")
          ],
          [
‎             ("نسخه")
          ]
]  


usersdb = mongodb.userstats

async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list
    
async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})
    
    
    
    

    
    
@bot.on_message(filters.command("stats") & filters.user(OWNER))
async def stats(client, message):
       m = await message.reply("**ثواني**")
       stats = len(await get_served_users())
       await m.edit(f"**- احصائيات المستخدمين : {stats}**")
           




@bot.on_message(filters.command("اذاعه", ["$", ""]) & filters.user(OWNER))
async def broadcast(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_users()
        for user in schats:
            chats.append(int(user["user_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"✶ تمت الاذاعه إلى {sent} مستخدم في البوت.")
        return
    if len(message.command) < 2:
        await message.reply_text(
‎            "**مثال**:\n\nاذاعه (`رسالتك`) او (`الرد على رساله`)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_users()
    for user in schats:
        chats.append(int(user["user_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"✶ تمت الاذاعه إلى {sent} مستخدم في البوت.")
    
    


             
@bot.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
       user_id = message.from_user.id
       if not await is_served_user(user_id):
         await add_served_user(user_id)
         stats = len(await get_served_users())
         await bot.send_message(OWNER, f"**-» قام شخص جديد بالدخول الى البوت الخاص بك :\n\n- -» اسمه : {message.from_user.mention}\n-» معرفه : @{message.from_user.username}\n-» ايديه : {message.from_user.id}\n➖ أصبح عدد مستخدمين البوت : ~ {stats}**")
       m = message.chat.id
       user = message.from_user.mention
       await message.reply(f"""**• هلا والله عيني {user}

‎- انا بوت احمل لك اي منشور مقيد المحتوى !
‎- احمل من القنوات والقروبات وبكل الصيغ سواء ملصق او صوره او صوت او فيديو وكل شي 
‎- فقط ارسل رابط المنشور المراد تحميله**""",
       disable_web_page_preview=True,
       reply_markup=InlineKeyboardMarkup(
                    [
                       [
                            InlineKeyboardButton("• شرح الاستخدام •", callback_data='test'),
                        ],[
                            InlineKeyboardButton("مطور البوت",user_id=2089102006)
                        ]
                    ]
                )
            )

@bot.on_callback_query(filters.regex("test"))
async def var(_, query: CallbackQuery):
      
    await query.edit_message_text("""**• شرح الاستخدام ↓**[ㅤ ](https://telegra.ph/file/bee49be69e475975b4bb1.mp4)""",
       reply_markup=InlineKeyboardMarkup(
                    [
                       [
                            InlineKeyboardButton("رجوع", callback_data='back'),

                        ]
                    ]
                )
            )

@bot.on_callback_query(filters.regex("back"))
async def back(_, query: CallbackQuery):
      
    await query.edit_message_text("""**• هلا والله عيني 
    
‎- انا بوت احمل لك اي منشور مقيد المحتوى !
‎- احمل من القنوات والقروبات وبكل الصيغ سواء ملصق او صوره او صوت او فيديو وكل شي 
‎- فقط ارسل رابط المنشور المراد تحميله**""",
       reply_markup=InlineKeyboardMarkup(
                    [
                       [
                            InlineKeyboardButton("• شرح الاستخدام •", callback_data='test'),
                        ],[
                            InlineKeyboardButton("مطور البوت",user_id=2089102006)
                        ]
                    ]
                )
            )
    
    
    

 
    
# download status
def downstatus(statusfile,message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile,"r") as downread:
            txt = downread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"- جاري التحميل : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)


# upload status
def upstatus(statusfile,message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile,"r") as upread:
            txt = upread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"**- جاري التحميل ..** : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)


# progress writter
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt',"w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")


@bot.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):

    # joining chats
    if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:

        try:
            with acc:
                acc.join_chat(message.text)
            bot.send_message(message.chat.id,"**- ابشر دخلت بنجاح ..**", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            bot.send_message(message.chat.id,"**- ياحلو انا فيه من زمان ..**", reply_to_message_id=message.id)
        except InviteHashExpired:
            bot.send_message(message.chat.id,"**- تأكد من الرابط ياحلو ..**", reply_to_message_id=message.id)
    
    # getting message
    elif "https://t.me/" in message.text:

        datas = message.text.split("/")
        msgid = int(datas[-1])

        # private
        if "https://t.me/c/" in message.text:
            chatid = int("-100" + datas[-2])

            with acc:
                msg  = acc.get_messages(chatid,msgid)

                if "text" in str(msg):
                    bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
                    return

                smsg = bot.send_message(message.chat.id, '** جاري التحميل ..**', reply_to_message_id=message.id)
                dosta = threading.Thread(target=lambda:downstatus(f'{message.id}downstatus.txt',smsg),daemon=True)
                dosta.start()
                file = acc.download_media(msg, progress=progress, progress_args=[message,"down"])
                os.remove(f'{message.id}downstatus.txt')

                upsta = threading.Thread(target=lambda:upstatus(f'{message.id}upstatus.txt',smsg),daemon=True)
                upsta.start()

            if "Document" in str(msg):
                try:
                    with acc:
                        thumb = acc.download_media(msg.document.thumbs[0].file_id)
                except:
                    thumb = None
                bot.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
                if thumb != None:
                    os.remove(thumb)

            elif "Video" in str(msg):
                try:
                    with acc:
                        thumb = acc.download_media(msg.video.thumbs[0].file_id)
                except:
                    thumb = None
                bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
                if thumb != None:
                    os.remove(thumb)

            elif "Animation" in str(msg):
                bot.send_animation(message.chat.id, file, reply_to_message_id=message.id)
               
            elif "Sticker" in str(msg):
                bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

            elif "Voice" in str(msg):
                bot.send_voice(message.chat.id, file, caption=msg.caption, thumb=thumb, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])

            elif "Audio" in str(msg):
                try:
                    with acc:
                        thumb = acc.download_media(msg.audio.thumbs[0].file_id)
                except:
                    thumb = None
                bot.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])   
                if thumb != None:
                    os.remove(thumb)

            elif "Photo" in str(msg):
                bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)


            os.remove(file)
            if os.path.exists(f'{message.id}upstatus.txt'):
                os.remove(f'{message.id}upstatus.txt')
            bot.delete_messages(message.chat.id,[smsg.id])
                
        
        # public
        else:
            username = datas[-2]
            msg  = bot.get_messages(username,msgid)
            
            if "Document" in str(msg):
                bot.send_document(message.chat.id, msg.document.file_id, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)

            elif "Video" in str(msg):
                bot.send_video(message.chat.id, msg.video.file_id, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)
            
            elif "Animation" in str(msg):
                bot.send_animation(message.chat.id, msg.animation.file_id, reply_to_message_id=message.id)

            elif "Sticker" in str(msg):
                bot.send_sticker(message.chat.id, msg.sticker.file_id, reply_to_message_id=message.id)

            elif "Voice" in str(msg):
                bot.send_voice(message.chat.id, msg.voice.file_id, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)    

            elif "Audio" in str(msg):
                bot.send_audio(message.chat.id, msg.audio.file_id, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)    

            elif "text" in str(msg):
                bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)

            elif "Photo" in str(msg):
                bot.send_photo(message.chat.id, msg.photo.file_id, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)


# infinty polling
print("تم التشغيل !")
bot.run()
