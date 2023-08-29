from pytube import YouTube
import os
from youtube_search import YoutubeSearch
import validators
import asyncio

async def getYTurl(search:str):
    valid = validators.url(search)
    if not valid:
        results = YoutubeSearch(search, max_results=1).to_dict()
        search = "https://youtube.com"+results[0]["url_suffix"]
    
    yt = YouTube(search)
    return [search, yt.title, yt.author, yt.length, yt.thumbnail_url]

 
async def url_download(url):
    yt = YouTube(url)
    
    video = yt.streams.filter(only_audio=True).first()
    
    out_file = video.download(output_path="songs")
    
    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"
    if not os.path.exists(new_file):
        os.rename(out_file, new_file)
    
    return new_file