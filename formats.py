import random as rd
import time
import discord
from discord.ext import commands


emojies = ["✨","🕺","💃", "🎶","✩","🎧","🎸","🎶","🍾"]
localEmojies = ["Edward2", "Herman", "Kristian", "Ludvig", "TheFuck", "edward", "kjekken", "kjekkenV2"]
emojiIds = [423387835924611072, 754734966440722464, 759827978954866698, 759828346342211614, 759828521269854248, 766774862496530472, 803601349710446612, 805778128446160926]
disco_colors = [
    "diff",
    "json",
    "yaml",
    "http",
    "arm",
    "diff",
    "css",
    "fix",
    "elm",
    "ini"
]

async def songQueue(queue):
    text = "```Song Queue:\n"
    
    for i in range(len(queue)):
        text += f"{i+1}. {queue[i][1]} - {queue[i][2]} {rd.choice(emojies)}\n"
        
    text += "```"
    return text

async def editPlaying(message, ctx):
    for i in range(100):
        time.sleep(0.1)
        
        emoji = await ctx.guild.fetch_emoji(rd.choice(emojiIds))
        color = rd.choice(disco_colors)
        
        edited_content = f"{emoji} {message.content} {emoji}"
        await message.edit(content = edited_content)

