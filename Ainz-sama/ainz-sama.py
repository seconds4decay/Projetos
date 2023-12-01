# ainz-sama.py


import os
os.system('cls')

import re # blibioteca usada na manipulação avançada de strings
import pathlib
import discord
from discord.ext import bot
from discord.ext import commands
import random # biblioteca usado no rodador de dado
import yt_dlp as youtube_dl #blibioteca usada pro youtube video player)
import asyncio # blibioteca usado em processos de threading(basicamente processos que ocorrem de fundo enquanto outros processos rodam)

path = pathlib.Path(__file__).parent.absolute()
file='token.txt'
token = open(f'{path}\{file}').read()

prefix = '>'
x = 1

# intents são permissões do bot, isso ai é pra liberar as permissões aqui
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

# configurações para o baixador de video 
ytdlopts = { 
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  
    'force-ipv4': True,
    'preferredcodec': 'mp3',
    'cachedir': False
    }
# configurações para o baixador de video 
ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = youtube_dl.YoutubeDL(ytdlopts) 

bot = commands.Bot(command_prefix=commands.when_mentioned_or('>'), intents=intents) #prefixos
bot.remove_command("help")


@bot.event # printa no terminal quando o bot está ligado
async def on_ready():
    print(f'Logged on as {bot.user}')


@bot.command(name='roll') # comando rolador de dado
async def roll(ctx, roll):
    num = re.findall('\d+', roll)
    op = re.findall('[+\-*/]', roll)
    num = [int(x) for x in num]
    numdice = num[0]
    a=1
    b=0
    if roll[1] == '#':
        b = 1
        a = num[0]
        numdice = num[1]
    for z in range(a):
        result = []
        for x in range(numdice):
            dice = random.randint(1, num[(1+b)])
            result.append(dice)
        if op is None:
            await ctx.message.reply(f'` {result} ` ⟵ [{result}] {roll}')
        elif '+' or '-' in op:
            opr = 0
            suma = num[2+b:len(num)]
            for x in range(len(suma)):
                if op[x] == '+':
                    opr += suma[x]
                elif op[x == '-']:
                    opr -= suma[x]
                elif op[x] == '*':
                    opr *= suma[x]
                elif op[x] == '/':
                    opr /= suma[x]
            await ctx.message.reply(f'` {opr+sum(result)} ` ⟵ { result } {roll}')

@bot.command(name='play') #comando de tocar video
async def play(ctx, *, query):
    try: 
        voice_channel = ctx.author.voice.channel #tenta entrar no canal
    except AttributeError: #caso o usuario nn esteja em um canal de voz e tente usar o comando
        return await ctx.send("Antes de usar esse comando, entre em um canal de voz primeiro.")

    permissions = voice_channel.permissions_for(ctx.me)
    if not permissions.connect or not permissions.speak: #caso o bot esteja sem permissão
        await ctx.send("Estou sem permissão para entrar nesse canal.")
        return
    
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await voice_channel.connect()
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    # cria um threading rodando as informações do baixador de video
    loop = asyncio.get_event_loop() 
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url=query, download=False))

    
    title = data['title']
    song = data['url']

    if 'entries' in data: #caso o link seja uma playlist, ele puxa o primeiro video
            data = data['entries'][0]

    try:
        voice_client.play(discord.FFmpegPCMAudio(source=song,**ffmpeg_options, executable="c:/ffmpeg/bin/ffmpeg")) # toca o video

    except Exception as e: # não faço a minima ideia doq seja isso
        print(e)
    await ctx.send(f'**Tocando:** {title}')

@bot.command(name='pause') #comando de pausar video
async def pause(ctx):
    voice_channel = ctx.message.guild.voice_client
    await voice_channelpause()

@bot.command(name='resume') #comando de resumir video
async def resume(ctx):
    voice_channel = ctx.message.guild.voice_client
    await voice_channel.resume()
    
@bot.command(name='stop') #comando de parar video
async def stop(ctx):
    voice_channel = ctx.message.guild.voice_client
    await voice_channel.disconnect()

@bot.command(name='playloop') #comando de loopar video
async def playloop(ctx, *, query):
    try: 
        voice_channel = ctx.author.voice.channel #tenta entrar no canal
    except AttributeError: #caso o usuario nn esteja em um canal de voz e tente usar o comando
        return await ctx.send("Antes de usar esse comando, entre em um canal de voz primeiro.")

    permissions = voice_channel.permissions_for(ctx.me)
    if not permissions.connect or not permissions.speak: #caso o bot esteja sem permissão
        await ctx.send("Estou sem permissão para entrar nesse canal.")
        return
    
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await voice_channel.connect()
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    # cria um threading rodando as informações do baixador de video
    loop = asyncio.get_event_loop() 
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url=query, download=False))

    
    title = data['title']
    song = data['url']

    if 'entries' in data: #caso o link seja uma playlist, ele puxa o primeiro video
            data = data['entries'][0]

    await ctx.send(f'**Tocando:** {title}')
    while True:
        try:
            voice_client.play(discord.FFmpegPCMAudio(source=song,**ffmpeg_options, executable="c:/ffmpeg/bin/ffmpeg")) # toca o video

        except Exception as e: # não faço a minima ideia doq seja isso
            print(e)
            break


bot.run(token) #ligar o bot