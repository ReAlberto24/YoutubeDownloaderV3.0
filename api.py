from typing import Any
import subprocess, os
def download(video_stream:Any, audio_stream:Any, codec:str, download_directory:str) -> None:
    # downloading streams
    if video_stream != None:
        print('Downloading video stream')
        video_stream.download(filename=f'video_stream.{codec}')
    print('Downloading audio stream'+' '*60)
    audio_stream.download(filename=f'audio_stream.{codec}')

    # convert to final .mp4 file
    print('Converting audio stream'+' '*60)
    subprocess.run(f'.\\ffmpeg -i .\\audio_stream.{codec} .\\audio_stream.wav -y', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if video_stream != None:
        print('Unifying video & audio streams')
        subprocess.run(f'.\\ffmpeg -i .\\video_stream.{codec} -i .\\audio_stream.wav -c:v copy -c:a aac ".\\{download_directory}\\{audio_stream.default_filename.rsplit(".")[0]}.mp4" -y', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    else:
        os.rename('.\\audio_stream.wav', f'.\\{download_directory}\\{audio_stream.default_filename.rsplit(".")[0]}.wav')

def rem_temp(codec:str) -> None:
    try: os.remove(f'audio_stream.wav')
    except: pass
    os.remove(f'audio_stream.{codec}')
    try: os.remove(f'video_stream.{codec}')
    except: pass