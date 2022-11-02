from pytube import YouTube
from pytube.cli import on_progress
import subprocess

#link = 'https://www.youtube.com/watch?v=tqK5VoEyDQU'
#link = 'https://www.youtube.com/watch?v=lJVGd7cBGuQ'
link = input('video link: ')
yt = YouTube(link, on_progress_callback=on_progress)

video_streams = []
audio_streams = []

for i in yt.streams.filter(progressive=False):
    if i.type == 'video': video_streams.append(i)
    elif i.type == 'audio': audio_streams.append(i)
    else: raise Exception('Invalid stream type')

with open(f'ext.xml', 'w') as file:
    for i in yt.streams:
        file.write(str(i)+'\n')

# mp4 or webm
# webm limits:
#     video: 4k or UHD
#     audio: 160kbps
# mp4 limits:
#     video: 8k
#     audio: 128kbps
codec = 'webm'

codec_video_streams = []
codec_audio_streams = []

for i in video_streams:
    if i.mime_type == f'video/{codec}':
        #print(i.itag, i.resolution, i.fps, i.codecs)
        codec_video_streams.append(i)

for i in audio_streams:
    if i.mime_type == f'audio/{codec}':
        #print(i.itag, i.abr, i.mime_type)
        codec_audio_streams.append(i)

# get file name: stream.default_filename

for i, x in enumerate(codec_video_streams):
    print(i, x.resolution, str(x.fps)+'fps')
#print(codec_video_streams)
video_stream = codec_video_streams[ int( input(': ') ) ]
audio_stream = codec_audio_streams[::-1][0]

#downloading streams
print('Video stream'+' '*70)
video_stream.download(filename=f'video_stream.{codec}')
print('Audio stream'+' '*70)
audio_stream.download(filename=f'audio_stream.{codec}')
print()

subprocess.run(f'.\\ffmpeg -i video_stream.{codec} -i audio_stream.{codec} -c copy "{video_stream.default_filename.rsplit(".")[0]}.mp4" -y', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)