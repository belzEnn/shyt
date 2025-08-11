import discord
from discord.ext import commands
import random
from config import EMOJI_LIST, REACTION_CHANCE
from utils import send_random_meme_to_channel

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_counter = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if random.random() < REACTION_CHANCE:
            random_emoji = random.choice(EMOJI_LIST)
            await message.add_reaction(random_emoji)
        if not message.content.startswith(self.bot.command_prefix):
            self.message_counter += 1
        if self.bot.user in message.mentions:
            embed = discord.Embed(
                description=(f"### {self.bot.user.mention}\nПрефикс бота: **!**\nДля просмотра команд бота используйте `!хелп`."),
                color=10027247
            )
            await message.channel.send(embed=embed)
        if self.message_counter % 10 == 0 and self.message_counter > 0:
            print(f"[{self.message_counter} сообщений] Отправляю случайный мем...")
            await send_random_meme_to_channel(self.bot, message.channel)
            self.message_counter = 0

    @commands.command(name='хелп')
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="== Команды бота ==",
            description=("**Префикс - !**\nпоиск - поиск запроса по википедии\nперевод - перевод через **Google Translate**\nпинг - узнать текущий пинг бота\nplay [URL] - воспроизвести музыку из YouTube в ГС\nstop - остановить музыку и отключиться от ГС\nмем - получить случайный мем из канала приколов"),
            color=10027247)
        await ctx.send(embed=embed)

    @commands.command(name='пинг', aliases=['ping'])
    async def ping(self, ctx):
        latency = self.bot.latency * 1000
        await ctx.send(f"Понг! {latency:.2f}ms")

async def setup(bot):
    await bot.add_cog(General(bot))
