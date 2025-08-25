import discord
from discord.ext import commands
import wikipedia

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='поиск', aliases=['вики'])
    async def search(self, ctx, *, query: str):
        wikipedia.set_lang("ru")
<<<<<<< HEAD
        try:
            page = wikipedia.page(query)
            search_result = wikipedia.summary(query, sentences=10)

            embed = discord.Embed(
                title=f"<:search:1325923106619129997> {query}",
                description=search_result,
                color=discord.Color.blue(),
                url=page.url
            )
            await ctx.send(embed=embed)

        except wikipedia.exceptions.PageError:
            embed = discord.Embed(
                title="<:error:1325917860492738712> Ошибка",
                description="Страница не найдена.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="<:error:1325917860492738712> Ошибка",
                description=str(e),
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Search(bot))
=======
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
>>>>>>> c1f4b12d4babc3b7d9da41bc20eae42f630c68b4
