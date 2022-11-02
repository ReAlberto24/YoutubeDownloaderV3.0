@echo off
echo Downloading ffmpeg
curl https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-2022-10-30-git-ed5a438f05-full_build.7z --output ffmpeg-git-full.7z --ssl-no-revoke
echo Decompressing ffmpeg
.\7z.exe x .\ffmpeg-git-full.7z
echo Moving ffmpeg
move .\ffmpeg-2022-10-30-git-ed5a438f05-full_build\bin\ffmpeg.exe .\ffmpeg.exe
echo Removing temp files
rd /Q /S .\ffmpeg-2022-10-30-git-ed5a438f05-full_build
del /Q .\ffmpeg-git-full.7z