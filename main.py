import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaVideo

import time
import os
import threading

bot_token = os.environ.get("TOKEN", "5893575537:AAHmT8eCW2VJFrSPfnG_vKV2HL_ExOsxjJc") 
api_hash = os.environ.get("HASH", "82fd1b4d334c4b813572cb0b1fcc299d") 
api_id = os.environ.get("ID", "21886784")
ss = os.environ.get("STRING", "BQBw5aCrAUdPgX0-01p0ycErSUP-JVJeSv1O92S_gswcxE0SRYHeTDE-sGJM5RtDSl5_vHWAIwSyfuWAE0Z6oMUMLFPgNmcCt-nID6EsvYmHPf8VFJ0Qv1iSaSckdg-0Y0pW_AK9OMjaX2HPLDt5aVQLBTfrexbWPGjcxR3C2qFCuONXfgG199h7UGFm7XDoloJ4I_6bXrOVvPYkPumyleBL7dH731WVSeJfwjFsVQj-J067E-WYsNE0KsGRoBn2WEd9H4LvD0ftK_EgJU7h-7EXFbV1LcjTU_6QZbJ2dMm69-skUgXBrNRRuSi17kly662yqeH0dH3BqJxIVT9hHxL2AAAAAVfems0A")
bot = Client("mybot",api_id=api_id,api_hash=api_hash,bot_token=bot_token)
acc = Client("myacc",api_id=api_id,api_hash=api_hash,session_string=ss)





@bot.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
       m = message.chat.id
       user = message.from_user.mention
       await message.reply(f"""**• هلا والله عيني {user}

- انا بوت احمل لك اي منشور مقيد المحتوى !
- احمل من القنوات والقروبات وبكل الصيغ سواء ملصق او صوره او صوت او فيديو وكل شي 
- فقط ارسل رابط المنشور المراد تحميله**""",
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
      
    await query.edit_message_text("""**• شرح الاستخدام ↓**[ㅤ ](https://telegra.ph/file/3f991cf109e90c025f35a.mp4)""",
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
    
- انا بوت احمل لك اي منشور مقيد المحتوى !
- احمل من القنوات والقروبات وبكل الصيغ سواء ملصق او صوره او صوت او فيديو وكل شي 
- فقط ارسل رابط المنشور المراد تحميله**""",
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
            bot.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
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
            bot.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
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
            bot.send_message(message.chat.id,"**Chat Joined**", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            bot.send_message(message.chat.id,"**Chat alredy Joined**", reply_to_message_id=message.id)
        except InviteHashExpired:
            bot.send_message(message.chat.id,"**Invalid Link**", reply_to_message_id=message.id)
    
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

                smsg = bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
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
print("Done !")
bot.run()
