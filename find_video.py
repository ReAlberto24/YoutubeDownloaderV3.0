import urllib.request
import urllib.parse
import re

from pytube import YouTube
from pytube.cli import on_progress
from getpass import getuser
import subprocess, os, yaml

# loading conf
config = yaml.safe_load(
    open('conf.yaml', 'r')
)

# loading download directory
try:
    download_directory = int(config['download_directory'])
    if download_directory:
        try: os.mkdir('.\\downloads')
        except: pass
        download_directory = '.\\downloads'
    else:
        download_directory = f'C:\\Users\\{getuser()}\\Downloads'
except:
    download_directory = str(config['download_directory']).replace('%u', getuser())

# starting program + starting pytube
vid_find = urllib.parse.quote(input('Video to find: '))
html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={vid_find}')
videos_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
link = f'https://www.youtube.com/watch?v={videos_ids[0]}'

yt = YouTube(link, on_progress_callback=on_progress)

video_streams = []
audio_streams = []

# getting audio & video streams from pytube
for i in yt.streams.filter(progressive=False):
    if i.type == 'video':    video_streams.append(i)
    elif i.type == 'audio':  audio_streams.append(i)
    else:                    raise Exception('Invalid stream type')

with open(f'ext.xml', 'w') as file:
    file.write('\n'.join(
        map(str, yt.streams)
        ))

codec = config['codec']

codec_video_streams = []
codec_audio_streams = []

if int(input('only audio (0: no, 1: yes): ')):
    # get all audio streams with config codec
    for i in audio_streams:
        if i.mime_type == f'audio/{codec}':
            #print(i.itag, i.abr, i.mime_type)
            codec_audio_streams.append(i)
else:
    # get all video streams with config codec
    for i in video_streams:
        if i.mime_type == f'video/{codec}':
            #print(i.itag, i.resolution, i.fps, i.codecs)
            codec_video_streams.append(i)

    # get all audio streams with config codec
    for i in audio_streams:
        if i.mime_type == f'audio/{codec}':
            #print(i.itag, i.abr, i.mime_type)
            codec_audio_streams.append(i)

codec_audio_streams = codec_audio_streams[::-1]

video_stream = None
audio_stream = None

if len(codec_video_streams) > 0:
    # get requested resolution
    for i, x in enumerate(codec_video_streams):
        print(i, x.resolution, str(x.fps)+'fps')
    #print(codec_video_streams)
    video_stream = codec_video_streams[ int( input(': ') ) ]
    audio_stream = codec_audio_streams[0]
else:
    # get requested resolution
    for i, x in enumerate(codec_audio_streams):
        print(i, x.abr)
    #print(codec_audio_streams)
    audio_stream = codec_audio_streams[ int( input(': ') ) ]

# downloading streams
if video_stream != None:
    print('Downloading video stream')
    video_stream.download(filename=f'video_stream.{codec}')
print('Downloading audio stream'+' '*60)
audio_stream.download(filename=f'audio_stream.{codec}')

# convert to final .mp4 file
print('Converting audio stream'+' '*60)
subprocess.run(f'.\\ffmpeg -i .\\audio_stream.{codec} .\\audio_stream.mp3 -y', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
if video_stream != None:
    print('Unifying video & audio streams')
    subprocess.run(f'.\\ffmpeg -i .\\video_stream.{codec} -i .\\audio_stream.mp3 -c copy ".\\{download_directory}\\{audio_stream.default_filename.rsplit(".")[0]}.mp4" -y', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
else:
    os.rename('.\\audio_stream.mp3', f'.\\{download_directory}\\{audio_stream.default_filename.rsplit(".")[0]}.mp3')

# removing temp files
print('Removing temp files')
try: os.remove(f'audio_stream.mp3')
except: pass
os.remove(f'audio_stream.{codec}')
try: os.remove(f'video_stream.{codec}')
except: pass