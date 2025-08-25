from discord.ext import commands
from googletrans import Translator, LANGUAGES
import discord  

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='перевод', aliases=['п'])
    async def translate(self, ctx, *, text: str = None):
        try:
            # Если это ответ на другое сообщение, переводим его
            if ctx.message.reference and not text:
                replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                text = replied_message.content
            # Если нету текста
            if not text:
                embed = discord.Embed(
                    title="<:error:1325917860492738712> Ошибка",
                    description="Нет текста для перевода.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            # проверка языка
            translator = Translator()
            detected_lang = translator.detect(text).lang
            target_lang = 'ru' if detected_lang != 'ru' else 'en'
            result = translator.translate(text, dest=target_lang)
            # Отп
            embed = discord.Embed(
                title=f"<:translate:1325918792731328522> {detected_lang} → {target_lang}",
                description=result.text,
                color=discord.Color.blue()
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
    await bot.add_cog(Translate(bot))
