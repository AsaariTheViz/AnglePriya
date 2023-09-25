# pylint: disable=C0321, broad-except, missing-docstring, import-error, unused-variable, unused-argument, too-many-arguments, too-many-instance-attributes, too-many-public-methods, too-many-boolean-expressions, too-many-lines, too-many-function-args, too-many-ancestors, no-member, line-too-long, undefined-variable

# MIT License

# Copyright (c) 2023 Rahul Thakor

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

import os
import math
import json
import time
import shutil
import random
import aiohttp
import threading
import asyncio
import requests
from pyrogram import enums
from Uploader.utitles import *
from Uploader.config import Config
from Uploader.config import TOTAL_TASKS
from Uploader.script import Translation
from Uploader.functions.database import *
from Uploader.bypasser import get_details, final_url
from Uploader.functions.thumb_help import Take_screen_shot, Get_video_dimensions
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from Uploader.functions.display_progress import progress_for_pyrogram as progress2, humanbytes, TimeFormatter

video_formats = [
    "MP4", "MOV", "WMV", "AVI", "AVCHD", "FLV", "F4V", "SWF", "MKV"
]
audio_formats = ["MP3", "WAV", "AIFF", "FLAC", "AAC", "WMA", "OGG", "M4A"]


# sourcery skip: low-code-quality
async def ddl_call_back(bot, query: CallbackQuery, is_message=False, link=None):

    if not hasattr(query, 'message'):
        msg = query
        await msg.reply_to_message.delete()
    else:
        msg = query.message
        await msg.delete()

    download_url = link or await final_url(msg.reply_to_message.text)

    download_url = await final_url(download_url)

    user_id = msg.from_user.id

    file_name, file_extention, file_size, content_type = await get_details(download_url)

    if is_message:
        file_msg = msg.text.split(".")
        file_name = f"{msg.text}.{file_extention}" if len(
            file_msg) < 2 else msg.text
    thumb_id = find_any(user_id, "PHOTO_THUMB")
    caption = None  # find_any(user_id, "CAPTION")

    if not caption:
        caption = file_name

    video_dir, status, thumb_path = random_dirs(user_id)

    if not os.path.isdir(video_dir):
        os.makedirs(video_dir)
    video_path = f"{video_dir}/{file_name}"

    msg_id = msg.reply_to_message.reply_to_message_id

    sent_message = await msg.reply_text(reply_to_message_id=msg_id,
                                        text=Translation.DOWNLOAD_START.format(file_name), parse_mode=enums.ParseMode.MARKDOWN)

    try:
        with open(status, 'w') as f:
            statusMsg = {'running': True, 'message': sent_message.id}
            json.dump(statusMsg, f, indent=2)
    except:
        pass
    async with aiohttp.ClientSession() as session:
        d_start = time.time()
        try:
            await download_coroutine(bot, session, download_url, video_path,
                                     user_id, sent_message.id, d_start, status)

        except asyncio.TimeoutError:
            await sent_message.edit_text(text=Translation.SLOW_URL_DECED)

    await sent_message.edit_text("Downloaded file, now uploading")
    up_time = time.time()

    if 'video' in content_type:
        width, height, duration = await Get_video_dimensions(video_path)
        thumbnail = await Take_screen_shot(video_path, thumb_path)
        await sent_message.reply_video(video_path, caption=caption, parse_mode=enums.ParseMode.MARKDOWN, reply_to_message_id=msg_id, width=width, height=height, duration=duration, thumb=thumbnail, progress=progress2, progress_args=(Translation.UPLOAD_START.format(file_name), sent_message,
                                                                                                                                                                                                                                        up_time, bot, user_id, status))

    await sent_message.delete()
    try:
        shutil.rmtree(video_dir)
    except Exception:
        pass


async def download_file(url, msg, file_name, start_t, d_msg, num_threads=1):
    """Download a file from a given URL using multi-connection"""

    # Get file size and calculate chunk size
    r = requests.head(url)

    size = int(r.headers.get('content-length', 0))
    chunk_size = size // num_threads

    # Create a list of threads to download each chunk
    threads = []
    with requests.get(url, stream=True) as r:
        # Set up progress tracking variables
        downloaded = 0
        progress_lock = threading.Lock()

        # Define function to download a single chunk
        def download_chunk(start, end):
            nonlocal downloaded
            headers = {'Range': f'bytes={start}-{end}'}
            with requests.get(url, headers=headers, stream=True) as r:
                r.raise_for_status()
                with open(file_name, 'wb') as f:
                    f.seek(start)
                    for chunk in r.iter_content(chunk_size=8192):
                        if not chunk:
                            break
                        f.write(chunk)
                        with progress_lock:
                            downloaded += len(chunk)
                            percent = downloaded / size * 100

                            r_percent = round(percent)
                            if (r_percent % 10 == 0):
                                time1 = time.time() - start_t  # 15

                                rem = size - downloaded  # load

                                speed = (downloaded / time1) / (1024)
                                speed1 = speed * 1024
                                eta_time = ((rem / speed) // 1024) * 1000
                                eta_time = round(eta_time)

                                progress = "[{0}{1}]\n**Progress :** {2}%\n".format(
                                    ''.join(["◾" for i in range(math.floor(percent / 10))
                                             ]),  # 7.6923
                                    ''.join(
                                        ["◽" for i in range(10 - math.floor(percent / 10))]),
                                    round(percent, 2))

                                tmp = progress + "**Completed :** {0} of {1}\n**Speed :** {2}/s\n**ETA :** {3}\n".format(
                                    humanbytes(downloaded), humanbytes(
                                        size), humanbytes(speed1),
                                    TimeFormatter(eta_time))
                                print(tmp)

                                try:
                                    msg.edit_text(tmp)
                                except Exception as ex:
                                    print(ex)

        # Start a thread for each chunk
        for i in range(num_threads):
            start = i * chunk_size
            end = start + chunk_size - 1 if i < num_threads - 1 else size - 1
            thread = threading.Thread(target=download_chunk, args=(start, end))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    return file_name


async def download_coroutine(bot, session, url, file_name, chat_id, message_id,
                             start, status):
    try:

        downloaded = 0
        # display_message = ""
        cancel_button = InlineKeyboardButton(
            "Cancel", callback_data=f"cancel_upload#{status}")

        reply_markup = InlineKeyboardMarkup([[cancel_button]])
        name = file_name.split("/")[-1]

        ud_type = f"**File Name:** {name}\n\n**Downloading...**\n"
        async with session.get(url,
                               timeout=Config.PROCESS_MAX_TIMEOUT) as response:

            total_length = int(response.headers["Content-Length"], 0)
            # print(response.headers)
            try:
                content_type = response.headers["Content-Type"]  # Content-Type
            except:
                content_type = 'video'
            if "text" in content_type or total_length < 500:
                return await response.release()
            with open(file_name, "wb") as f_handle:
                while True:
                    chunk = await response.content.read(Config.CHUNK_SIZE)
                    if not chunk:
                        break
                    f_handle.write(chunk)
                    downloaded += Config.CHUNK_SIZE

                    now = time.time()
                    diff = now - start
                    if round(diff % 5.0) == 0 or downloaded == total_length:
                        if os.path.exists(status):
                            with open(status, 'r+') as f:
                                statusMsg = json.load(f)
                                if not statusMsg["running"]:
                                    return await response.release()

                        percentage = downloaded * 100 / total_length
                        speed = downloaded / diff
                        # print(speed)
                        elapsed_time = round(diff) * 1000
                        time_to_completion = (round(
                            (total_length - downloaded) / speed) * 1000)
                        estimated_total_time = elapsed_time + time_to_completion
                        progress = "[{0}{1}]\n**Progress :** {2}%\n".format(
                            # 7.6923
                            ''.join(["◾️" for i in range(
                                math.floor(percentage / 10))]),
                            ''.join(["◽️" for i in range(
                                10 - math.floor(percentage / 10))]),
                            round(percentage, 2))

                        tmp = progress + "**Completed :** {0} of {1}\n**Speed :** {2}/s\n**ETA :** {3}\n".format(
                            humanbytes(downloaded), humanbytes(total_length),
                            humanbytes(speed), TimeFormatter(time_to_completion))

                        text = "{}{}".format(ud_type, tmp)
                        try:
                            await bot.edit_message_text(chat_id,
                                                        message_id,
                                                        text=text,
                                                        reply_markup=reply_markup,
                                                        parse_mode=enums.ParseMode.MARKDOWN)
                        except:
                            pass
            return await response.release()

    except Exception as ex:
        await bot.edit_message_text(chat_id, message_id, text=str(ex))
