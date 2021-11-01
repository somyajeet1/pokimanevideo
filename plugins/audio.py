Python 3.10.0 (tags/v3.10.0:b494f59, Oct  4 2021, 19:00:18) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import os
import re
import sys
import ffmpeg
import asyncio
import subprocess
from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import Message
from helpers.bot_utils import USERNAME
from config import AUDIO_CALL, VIDEO_CALL
from plugins.video import ydl, group_call
from helpers.decorators import authorized_users_only, sudo_users_only
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


@Client.on_message(filters.command(["play", f"play@{USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def play(client, m: Message):
    msg = await m.reply_text("🎥 Wᴀɪᴛ Kʀʀ Vɪᴅᴇᴏ Cʜᴀʟᴇɢᴀ ᴠᴄ Pʀ𝘁𝗶𝘁" 𝗞𝗿𝗿 𝗩𝗶𝗱𝗲𝗼 )𝗖𝗵𝗮𝗹𝗲𝗴𝗮 𝘃𝗰 𝗣𝗿
    chat_id = m.chat.id
    media = m.reply_to_message
    if not media and not ' ' in m.text:
        await msg.edit("❗ __Send Me An Live Radio Link / YouTube Video Link / Reply To An Audio To Start Audio Streaming!__")

    elif ' ' in m.text:
        text = m.text.split(' ', 1)
        query = text[1]
        if not 'http' in query:
            return await msg.edit("❗ 📩 Sᴇɴᴅ /sᴛʀᴇᴀᴍ Yᴏᴜᴛᴜʙᴇ Vɪᴅᴇᴏ Lɪɴᴋ OR Rᴇᴘʟʏ Tᴏ Aɴ Vɪᴅᴇᴏ Tᴏ Sᴛᴀʀᴛ Vɪᴅᴇᴏ Sᴛʀᴇᴀᴍɪɴɢ! Nᴏᴏʙ")
        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, query)
        if match:
            await msg.edit("🔊 Aᴜᴅɪᴏ Sᴛʀᴇᴀᴍ Cʜᴀʟᴇɢᴀ Wᴀɪᴛ...`")
            try:
                meta = ydl.extract_info(query, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                    ytstreamlink = f['url']
                link = ytstreamlink
            except Exception as e:
                return await msg.edit(f"❌ **YouTube Download Error LoL !** \n\n`{e}`")
                print(e)

        else:
            await msg.edit("🔊 Aᴜᴅɪᴏ Sᴛʀᴇᴀᴍ Cʜᴀʟᴇɢᴀ Wᴀɪᴛ...`")
            link = query

        vid_call = VIDEO_CALL.get(chat_id)
        if vid_call:
            await VIDEO_CALL[chat_id].stop()
            VIDEO_CALL.pop(chat_id)
            await sleep(3)

        aud_call = AUDIO_CALL.get(chat_id)
        if aud_call:
            await AUDIO_CALL[chat_id].stop()
            AUDIO_CALL.pop(chat_id)
            await sleep(3)

        try:
            await sleep(2)
            await group_call.join(chat_id)
            await group_call.start_audio(link, repeat=False)
            AUDIO_CALL[chat_id] = group_call
            await msg.delete()
            await m.reply_text(f"▶️ **Started [Audio Streaming]({query}) In {m.chat.title} !**",
               reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton(
                          text="⏸",
                          callback_data="pause_callback",
                       ),
                       InlineKeyboardButton(
                          text="▶️",
                          callback_data="resume_callback",
                       ),
                       InlineKeyboardButton(
                          text="⏹️",
                          callback_data="end_callback",
                       ),
                   ],
               ]),
            )
        except Exception as e:
            await msg.edit(f"❌ **An Error Occoured LoL !** \n\nError: `{e}`")
            return await group_call.stop()

    elif media.audio or media.document:
        await msg.edit("🔄 `Downloading  wait..`")
        audio = await client.download_media(media)

        vid_call = VIDEO_CALL.get(chat_id)
        if vid_call:
            await VIDEO_CALL[chat_id].stop()
            VIDEO_CALL.pop(chat_id)
            await sleep(3)

        aud_call = AUDIO_CALL.get(chat_id)
        if aud_call:
            await AUDIO_CALL[chat_id].stop()
            AUDIO_CALL.pop(chat_id)
            await sleep(3)

        try:
            await sleep(2)
            await group_call.join(chat_id)
            await group_call.start_audio(audio, repeat=False)
            AUDIO_CALL[chat_id] = group_call
            await msg.delete()
            await m.reply_text(f"▶️ **Started [Audio Streaming](https://t.me/AsmSafone) In {m.chat.title} !**",
               reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton(
                          text="⏸",
                          callback_data="pause_callback",
                       ),
                       InlineKeyboardButton(
                          text="▶️",
                          callback_data="resume_callback",
                       ),
                       InlineKeyboardButton(
                          text="⏹️",
                          callback_data="end_callback",
                       ),
                   ],
               ]),
            )
        except Exception as e:
            await msg.edit(f"❌ **An Error Occoured !** \n\nError: `{e}`")
            return await group_call.stop()

    else:
        await msg.edit(
            "💁🏻‍♂️ Dᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇᴀʀᴄʜ ғᴏʀ ᴀ YᴏᴜTᴜʙᴇ sᴏɴɢ ?"
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Yes", switch_inline_query_current_chat=""
                    ),
                    InlineKeyboardButton(
                        "No ❌", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_message(filters.command(["restart", f"restart@{USERNAME}"]))
@sudo_users_only
async def restart(client, m: Message):
    k = await m.reply_text("Rᴇsᴛᴀʀᴛɪɴɢ Wᴀɪᴛ Pʟᴇᴀsᴇ ‼️")
    await sleep(3)
    os.execl(sys.executable, sys.executable, *sys.argv)
    try:
        await k.edit("✅ **Restarted Successfully! \nJoin @teamDlt For More!**")
    except:
        pass
