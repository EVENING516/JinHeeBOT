import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time

bot = commands.Bot(command_prefix='*')

user = []
musictitle = []
song_queue = []
musicnow = []

def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    chromedriver_dir = r"C:\Users\UserK\Documents\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_dir, options = options)
    driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()
    
    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']

    driver.quit()
    
    return music, URL

def play(ctx):
    global VoiceChannel
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    VoiceChannel = get(bot.voice_clients, guild=ctx.guild)
    if not VoiceChannel.is_playing():
        VoiceChannel.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx)) 

def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not VoiceChannel.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            VoiceChannel.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("여자친구 찾기"))

@bot.command()
async def 따라하기(ctx, *, text):
    await ctx.send(text)

@bot.command()
async def 들어와(ctx):
    try:
        global VoiceChannel
        VoiceChannel = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await VoiceChannel.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("야임마 너가 어디있는지 알아야 들어가지!")

@bot.command()
async def 나가(ctx):
    try:
     await VoiceChannel.disconnect()
    except:
        await ctx.send("도대체 어디를 나가라는거야!")

@bot.command()
async def URL재생(ctx, *, url):

    try:
        global VoiceChannel
        VoiceChannel = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await VoiceChannel.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("야임마 너가 어디있는지 알아야 들어가지!")

    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not VoiceChannel.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        VoiceChannel.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "지금 " + url + "을(를) 부르고 있음.", color = 0x00ff00))
    else:
        await ctx.send("음악 이미 재생됐는데 뭐함")

@bot.command()
async def 재생(ctx, *,msg):

    try:
        global VoiceChannel
        VoiceChannel = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await VoiceChannel.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("야임마 너가 어디있는지 알아야 들어가지!")

    if not VoiceChannel.is_playing():
        global entireText
        YDL_OPTIONS = {'format':'bestaudio','noplatlist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        chromedriver_dir = r"C:\Users\UserK\Documents\chromedriver_win32\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir)
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get("href")
        url = 'https://www.youtube.com'+musicurl

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url,download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "지금 " + entireText + "을(를) 부르고있음 ", color = 0x00ff00))
        VoiceChannel.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        user.append(msg)
        result, URLTEST = title(msg)
        song_queue.append(URLTEST)

@bot.command()
async def 일시정지(ctx):
    if VoiceChannel.is_playing():
        VoiceChannel.pause()
        await ctx.send(embed = discord.Embed(title= "일시정지", description = entireText + "을(를) 일시정지 함", color = 0x00ff00))
    else:
        await ctx.send("지금 노래 안부르고 있음")

@bot.command()
async def 다시재생(ctx):
    try:
        VoiceChannel.resume()
    except:
     await ctx.send("지금 노래 안부르고 있음 ")
    else:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = entireText  + "을(를) 다시 재생함", color = 0x00ff00))

@bot.command()
async def 노래끄기(ctx):
    if VoiceChannel.is_playing():
        VoiceChannel.stop()
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = entireText  + "을(를) 종료함", color = 0x00ff00))
    else:
        await ctx.send("지금 노래 안부르고 있음")

@bot.command()
async def 지금노래(ctx):
    if not VoiceChannel.is_playing():
        await ctx.send("지금 노래 안부름.")
    else:
        await ctx.send(embed = discord.Embed(title = "지금노래", description = "현재 " + entireText + "을(를) 부르고 있음", color = 0x00ff00))

@bot.command()
async def 대기열추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(result + "를 재생목록에 함")

@bot.command()
async def 대기열삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]
            
        await ctx.send("대기열 삭제함")
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없어서 삭제 못함")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록개수를 벗어났슴!!")
            else:
                await ctx.send("숫자 써")

@bot.command()
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무노래도 안넣음")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "노래목록", description = Text.strip(), color = 0x00ff00))

@bot.command()
async def 목록초기화(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(embed = discord.Embed(title= "목록초기화", description = """목록 초기화 했음 이제 음악 넣으셈""", color = 0x00ff00))
    except:
        await ctx.send("아직 아무노래도 안넣음.")

@bot.command()
async def 목록재생(ctx):

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if len(user) == 0:
        await ctx.send("아직 아무노래도 안넣음.")
    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        if not VoiceChannel.is_playing():
            play(ctx)
        else:
            await ctx.send("노래가 이미 재생되고 있음")

bot.run('OTQ2NDMyNDgwMDAzNjMzMTcy.Yhen7w.ZS9TrvktkfbNg_AcEAeMX1M2O9Q')