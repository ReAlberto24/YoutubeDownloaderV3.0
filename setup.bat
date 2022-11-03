@echo off
IF EXIST ffmpeg.exe (
    echo setup was already run
    pause
    exit
) ELSE (
    echo running .\download_ffmpeg.bat
    .\download_ffmpeg.bat
    echo setup completed
    pause
    exit
)