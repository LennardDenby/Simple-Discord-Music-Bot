import discord
import json
import asyncio
import ytDownloader
import formats
from discord import FFmpegPCMAudio
from discord.ext import commands

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(intents=intents, command_prefix = "!")

songQueue = []

with open("creds.json") as f:
    creds = json.load(f)

TOKEN = creds["token"]

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("Join a voice channel first")
        return
    
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
    
async def pause(voice_client:discord.voice_client):
    voice_client.pause()    

async def formatSongArg(args):
    return " ".join(args)

@bot.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("Bot is not connected to a voice channel")
        
@bot.command()
async def play(ctx, *args):
    voice_client = ctx.message.guild.voice_client
    
    if not voice_client or not voice_client.is_connected():
        await join(ctx)
        voice_client = ctx.message.guild.voice_client
    
    if voice_client.is_playing():
        await pause(voice_client)
    
    arg = await formatSongArg(args)
    songUrl = await ytDownloader.getYTurl(arg)
    
    if not songQueue:
        songQueue.append(songUrl)
    else:
        songQueue[0] = songUrl
    
    await playSong(ctx, songUrl)
    

async def playSong(ctx, songUrl):
    voice_client = ctx.message.guild.voice_client
    
    def after_play(error):
        if error:
            print(f"An error occurred: {error}")
        else:
            bot.loop.create_task(nextSong(ctx))
    
    song = await ytDownloader.url_download(songUrl[0])
    
    emoji = await ctx.guild.fetch_emoji("524954164468514836")
    
    await ctx.send(f"{emoji} Now playing: **{songUrl[1]} - {songUrl[2]}** {emoji}")
    
    voice_client.play(discord.FFmpegPCMAudio(source=song), after = after_play)

@bot.command()
async def q(ctx, *args):
    if not args:
        if not songQueue:
            await ctx.send("```No songs in queue```")
        else:
            await ctx.send(await formats.songQueue(songQueue))
        return
        
    voice_client = ctx.message.guild.voice_client
    
    if not voice_client or not voice_client.is_connected():
        await play(ctx, *args)
        return

    if voice_client.is_playing():
        arg = await formatSongArg(args)
        songUrl = await ytDownloader.getYTurl(arg)
        songQueue.append(songUrl)
        
        await ctx.send(f"Added **{songUrl[1]} - {songUrl[2]}** to queue")
        
async def nextSong(ctx):
    if len(songQueue) < 1:
        return
    
    songQueue.pop(0)
    
    await playSong(ctx, songQueue[0])
    
@bot.command()
async def skip(ctx):
    voice_client = ctx.message.guild.voice_client
    if len(songQueue) <= 1:
        await ctx.send("Can not skip - queue is empty")
        return
        
    await pause(voice_client)
    await nextSong(ctx)

@bot.command()
async def np(ctx):
    pass

bot.run(TOKEN)