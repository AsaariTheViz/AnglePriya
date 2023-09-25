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


# MIT License
# Copyright (c) 2023 Rahul Thakor
import random
from moviepy.editor import VideoFileClip


def generate_random_number(lenght):
    return random.randint(1, lenght)


# Take a screenshot from video for thumbnail
async def Take_screen_shot(video_file, output_directory, s_time=60):
    try:
        s_time = generate_random_number(s_time)
        clip = VideoFileClip(video_file)
        duration = round(clip.duration)
        if duration > 60:
            s_time = generate_random_number(duration - 1)

        clip.save_frame(output_directory, t=s_time)
        clip.close()
        return output_directory
    except:
        return None


async def Get_video_dimensions(video_path):
    try:
        clip = VideoFileClip(video_path)
        width, height = clip.size
        duration = round(clip.duration)
        clip.close()
        return width, height, duration
    except:
        return 320, 320, 0
