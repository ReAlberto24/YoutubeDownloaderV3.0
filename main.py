from sys import path as syspath; syspath.append('.')
from pytube import YouTube
from pytube.cli import on_progress
from getpass import getuser
import os, yaml
from api import download, rem_temp

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
link = input('video link: ')
yt = YouTube(link, on_progress_callback=on_progress)

print(yt.title)

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

print('Converting audio stream'+' '*60)
download(video_stream, audio_stream, codec, download_directory)

# removing temp files
print('Removing temp files')
rem_temp(codec)
print('video downloaded')