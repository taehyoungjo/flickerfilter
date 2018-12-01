from __future__ import unicode_literals
import youtube_dl

def download(str):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([str])
    return True