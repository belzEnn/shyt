import discord
from discord.ext import commands
import wikipedia

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='поиск', aliases=['вики'])
    async def search(self, ctx, *, query: str):
        wikipedia.set_lang("ru")
        page = wikipedia.page(query)
        search_result = wikipedia.summary(query, sentences=10)
        embed = discord.Embed(
            title=f"<:search:1325923106619129997> {query}",
            description=search_result,
            color=discord.Color.blue(),
            url=page.url
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Search(bot))