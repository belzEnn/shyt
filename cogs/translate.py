from discord.ext import commands
from googletrans import Translator
import discord  

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='перевод', aliases=['translate'])
    async def translate(self, ctx, *, text: str = None):
        if ctx.message.reference:
            replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            text = replied_message.content
        translator = Translator()
        detected_lang = translator.detect(text).lang 
        target_lang = 'ru' if detected_lang != 'ru' else 'en'
        result = translator.translate(text, dest=target_lang) 
        embed = discord.Embed(
            title=f"<:translate:1325918792731328522> {detected_lang} > {target_lang}",
            description=result.text,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Translate(bot))