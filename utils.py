import random
import discord
from config import MEME_CHANNEL_IDS


async def send_random_meme_to_channel(bot, target_channel):
    selected_channel = None
    for channel_id in MEME_CHANNEL_IDS:
        channel = bot.get_channel(channel_id)
        if channel and isinstance(channel, discord.TextChannel):
            selected_channel = channel
            break
    if not selected_channel:
        await target_channel.send("Канал с мемами не найден.")
        return
    messages = []
    async for msg in selected_channel.history(limit=100):
        if msg.author == bot.user or msg.type != discord.MessageType.default:
            continue
        if msg.content or msg.attachments:
            messages.append(msg)
    if not messages:
        await target_channel.send("Не найдено подходящих мемов.")
        return
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
