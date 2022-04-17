import discord

from discord.utils import get 
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

from discord.ext import commands
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix='!',help_command=None)


message_lastseen = datetime.now()
message2_lastseen = datetime.now()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def help(ctx):
    emBed = discord.Embed(title="Command list",description="The default prefix of Rythm is !.", color=0xde8643)
    emBed.add_field(name='help',value="Get help command" , inline=False)
    emBed.add_field(name='user',value="Send Hi message to user" , inline=False)
    emBed.add_field(name='about',value="Let bot introduce myself" , inline=False)
    emBed.add_field(name='p,play',value="play music" , inline=False)
    emBed.add_field(name='stop',value="stop music" , inline=False)
    emBed.add_field(name='pause',value="Pauses the current playing track" , inline=False)
    emBed.add_field(name='resume',value="Resumes paused music." , inline=False)
    emBed.add_field(name='leave',value="Disconnects the bot from the voice channel it is in" , inline=False)
    emBed.set_thumbnail(url='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/4d21c2f4-1be5-4462-a3dc-a2ab0bc68112/de924s1-a704102d-e55a-4e6d-a15e-9b22555f0d8b.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzRkMjFjMmY0LTFiZTUtNDQ2Mi1hM2RjLWEyYWIwYmM2ODExMlwvZGU5MjRzMS1hNzA0MTAyZC1lNTVhLTRlNmQtYTE1ZS05YjIyNTU1ZjBkOGIucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.qX4diThCG_OtPoK8vt5CenPeuyIai-m6mSKUJ7eVeRU')
#    emBed.set_footer(text='test footer', icon_url='https://i.pinimg.com/originals/82/8c/5c/828c5c9543010265c82cb3e9a7e22539.jpg')
    await ctx.channel.send(embed=emBed)

@bot.event
async def on_message(message):
    global message_lastseen, message2_lastseen
    if message.content == '!hi':
        print(message.channel)
        await message.channel.send('Hello')
        print('test')
    elif message.content == '!user':
        await message.channel.send('Hi'+'    '+str(message.author.name))
    elif message.content == '!about'and datetime.now() >= message_lastseen:
        message_lastseen = datetime.now() + timedelta(seconds=5)
        await message.channel.send('I am ' + str(bot.user.name))
        print('{0} You use !about when {1} and will be available again when {2} '.format(message.author.name,datetime.now(),message_lastseen))
    elif message.content == 'what is my name' and datetime.now() >= message2_lastseen:
        messagw2_lastseen =datetime.now() + timedelta(seconds=5)
        await message.channel.send('Your name is  ' + str(message.author.name) )
    elif message.content == '!logout':
        await bot.logout()
    await bot.process_commands(message)

@bot.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if voice_client == None:
        await ctx.channel.send('Joined'+ '  ' +str(channel))
        await channel.connect()
        voice_client = get(bot.voice_clients, guild=ctx.guild)
 
    YDL_OPTIONS = {'formar' : 'bestaudio' , 'noplaylist' : 'False' }
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not voice_client.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice_client.is_playing()
    else :
        await ctx.channel.send("Already playing song")
        return

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()



bot.run('ODY5OTIxNTY5ODA2Mzg1MTcy.YQFPmA.dcmKp_c6DQkUwEkz0vp5VmQW6N4')