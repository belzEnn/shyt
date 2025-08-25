import discord
from discord.ext import commands
import wikipedia

class Photo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='фото', aliases=['photo'])
    async def photo(self, ctx, *, query: str):
        wikipedia.set_lang("ru")
        try:
            page = wikipedia.page(query)
            image_urls = [img for img in page.images if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not image_urls:
                await ctx.send("Изображения не найдены.")
                return
            embed = discord.Embed(
                title=f"<:search:1325923106619129997> {query}",
                color=discord.Color.blue(),
            )
            embed.set_image(url=image_urls[0])
            embed.set_footer(text=f"Источник: {page.url}")
            await ctx.send(embed=embed)
        except wikipedia.exceptions.PageError:
            await ctx.send("Страница не найдена.")
        except Exception as e:
            await ctx.send(f"Ошибка: {e}")