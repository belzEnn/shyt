# Импорт библиотек
import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
# Импорт cogs
from cogs import memes, translate, general, search, photo
from utils import send_random_meme_to_channel
# Загрузка переменных из .env
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

cogs = [general.General, memes.Memes, translate.Translate, search.Search, photo.Photo]

# Запуск бота
@bot.event
async def on_ready():
    # Регистрация cogs
    registered_cogs = set()
    for cog in cogs:
        if cog.__name__ not in registered_cogs:
            try:
                await bot.add_cog(cog(bot))  # Используем await
                registered_cogs.add(cog.__name__)
            except Exception as e:
                print(f"Не удалось загрузить cog {cog.__name__}: {e}")

    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="носик чайника"))
    print(f'Вошел как {bot.user}')

bot.run(os.getenv('DISCORD_TOKEN'))