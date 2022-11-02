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
link = input('video link: ')
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

# get requested resolution
for i, x in enumerate(codec_video_streams):
    print(i, x.resolution, str(x.fps)+'fps')
#print(codec_video_streams)
video_stream = codec_video_streams[ int( input(': ') ) ]
audio_stream = codec_audio_streams[::-1][0]

#downloading streams
print('Video stream')
video_stream.download(filename=f'video_stream.{codec}')
print('Audio stream'+' '*70)
audio_stream.download(filename=f'audio_stream.{codec}')

# convert to final .mp4 file
print('Converting audio stream'+' '*70)
subprocess.run(f'.\\ffmpeg -i .\\audio_stream.{codec} .\\audio_stream.mp3 -y', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
print('Unifying video & audio streams')
subprocess.run(f'.\\ffmpeg -i .\\video_stream.{codec} -i .\\audio_stream.mp3 -c copy ".\\{download_directory}\\{video_stream.default_filename.rsplit(".")[0]}.mp4" -y', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# removing temp files
print('Removing temp files')
os.remove(f'audio_stream.mp3')
os.remove(f'audio_stream.{codec}')
os.remove(f'video_stream.{codec}')