import discord
from discord.ext import commands
import asyncio
import yt_dlp as youtube_dl
import wikipedia
from googletrans import Translator
import random
import json
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Настройка для воспроизведения музыки
youtube_dl.utils.bug_reports_message = lambda: ''
FFMPEG_OPTIONS = {'options': '-vn'}
ytdl_format_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'extractaudio': True,
    'audioformat': 'mp3'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# Очередь воспроизведения
music_queue = []
current_song = None

# ID канала 'приколы'
MEME_CHANNEL_IDS = [
    1400544567949791334
]

# ID канала для отправки сообщений из консоли
CONSOLE_OUTPUT_CHANNEL_ID = 1400470917414392010

# ID целевого сервера
TARGET_GUILD_ID = 1400470915883728917

# Глобальный счетчик сообщений
message_counter = 0

# Список эмодзи для случайных реакций
EMOJI_LIST = [
    "🇮🇱", "🍆" 
]
REACTION_CHANCE = 0.1 # Шанс 10%

def get_target_guild():
    """Возвращает целевой сервер по ID."""
    return bot.get_guild(TARGET_GUILD_ID)

# Функция для сохранения голосовых каналов

async def console_input_listener():
    """
    Асинхронная функция для чтения ввода из консоли.
    """
    await bot.wait_until_ready()
    target_channel = bot.get_channel(CONSOLE_OUTPUT_CHANNEL_ID)

    if not target_channel:
        print(f"Ошибка: Канал для вывода из консоли с ID {CONSOLE_OUTPUT_CHANNEL_ID} не найден. Проверьте ID или права доступа бота.")
        return

    while not bot.is_closed():
        try:
            message_to_send = await asyncio.get_event_loop().run_in_executor(None, input, "Введите сообщение для отправки в Discord: ")
            
            if message_to_send:
                await target_channel.send(message_to_send)
                print(f"Сообщение отправлено: '{message_to_send}'")
        except Exception as e:
            print(f"Ошибка при обработке ввода из консоли: {e}")

@bot.event
async def on_ready():
    print(f'Вошел как {bot.user}')
    
    activity = discord.Game(name="носик чайника")
    await bot.change_presence(status=discord.Status.idle, activity=activity)

    bot.loop.create_task(console_input_listener())

@bot.event
async def on_message(message):
    global message_counter

    if message.author == bot.user:
        return

    if random.random() < REACTION_CHANCE:
        random_emoji = random.choice(EMOJI_LIST)
        await message.add_reaction(random_emoji)

    if not message.content.startswith(bot.command_prefix):
        message_counter += 1

    if bot.user in message.mentions:
        embed = discord.Embed(
            description=(f"### {bot.user.mention}\n"
                         "Префикс бота: !\n"
                         "Для просмотра команд бота используйте !хелп."),
            color=10027247
        )
        await message.channel.send(embed=embed)

    if message_counter % 10 == 0:
        print(f"[{message_counter} сообщений] Отправляю случайный мем...")
        await send_random_meme_to_channel(message.channel)
        message_counter = 0

    await bot.process_commands(message)


@bot.command(name='хелп')
async def help_command(ctx):
    embed = discord.Embed(
        title="== Команды бота ==",
        description=
        ("**Префикс - !**\n"
         "поиск - поиск запроса по википедии\n"
         "перевод - перевод через **Google Translate**\n"
         "пинг - узнать текущий пинг бота\n"
         "play [URL] - воспроизвести музыку из YouTube в ГС\n"
         "stop - остановить музыку и отключиться от ГС\n"
         "мем - получить случайный мем из канала приколов"
         ),
        color=10027247)
    await ctx.send(embed=embed)

@bot.command(name='пинг', aliases=['ping'])
async def ping(ctx):
    latency = bot.latency * 1000
    await ctx.send(f"Понг! {latency:.2f}ms")

@bot.command(name='перевод', aliases=['translate'])
async def translate(ctx, *, text: str = None):
    if ctx.message.reference:
        replied_message = await ctx.channel.fetch_message(
            ctx.message.reference.message_id)
        text = replied_message.content
    translator = Translator()
    detected_lang = translator.detect(text).lang
    target_lang = 'ru' if detected_lang != 'ru' else 'en'
    result = translator.translate(text, dest=target_lang)
    embed = discord.Embed(
        title=
        f"<:translate:1325918792731328522> {detected_lang} > {target_lang}",
        description=result.text,
        color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command(name='поиск', aliases=['вики'])
async def search(ctx, *, query: str):
    wikipedia.set_lang("ru")
    page = wikipedia.page(query)
    search_result = wikipedia.summary(query, sentences=10)
    embed = discord.Embed(
        title=f"<:search:1325923106619129997> {query}",
        description=search_result,
        color=discord.Color.blue(),
        url=page.url
    )
    embed.set_footer(text=f"Источник: {page.url}")
    await ctx.send(embed=embed)

@bot.command(name='фото', aliases=['photo'])
async def photo(ctx, *, query: str):
    wikipedia.set_lang("ru")
    page = wikipedia.page(query)
    image_urls = [img for img in page.images if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
    embed = discord.Embed(
        title=f"<:search:1325923106619129997> {query}",
        color=discord.Color.blue(),
    )
    embed.set_image(url=image_urls[0])
    embed.set_footer(text=f"Источник: {page.url}")
    await ctx.send(embed=embed)

async def send_random_meme_to_channel(target_channel):
    selected_channel = None
    for channel_id in MEME_CHANNEL_IDS:
        channel = bot.get_channel(channel_id)
        if channel and isinstance(channel, discord.TextChannel):
            selected_channel = channel
            break
    messages = []
    async for msg in selected_channel.history(limit=100):
        if msg.author == bot.user or msg.type != discord.MessageType.default:
            continue
        if msg.content or msg.attachments:
            messages.append(msg)
    random_message = random.choice(messages)
    sent_media = False
    if random_message.content:
        await target_channel.send(random_message.content)
    for attachment in random_message.attachments:
        if sent_media:
            break
        filename_lower = attachment.filename.lower()
        if filename_lower.endswith(('.png', '.jpg', '.jpeg')):
            photo_embed = discord.Embed(color=discord.Color.random())
            photo_embed.set_image(url=attachment.url)
            await target_channel.send(embed=photo_embed)
            sent_media = True
        elif filename_lower.endswith('.gif'):
            await target_channel.send(attachment.url)
            sent_media = True
    if not random_message.content and not sent_media:
        await target_channel.send("Выбранное сообщение-мем не содержало отображаемого контента (текст, фото или GIF).")

@bot.command(name='мем')
async def meme(ctx):
    await send_random_meme_to_channel(ctx.channel)

# Используем токен из переменной окружения
bot.run(os.getenv('DISCORD_TOKEN'))