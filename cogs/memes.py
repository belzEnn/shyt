from discord.ext import commands
from utils import send_random_meme_to_channel

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='мем')
    async def meme(self, ctx):
        await send_random_meme_to_channel(self.bot, ctx.channel)

async def setup(bot):
    await bot.add_cog(Memes(bot))
