import os
from dotenv import load_dotenv

load_dotenv()

# ID каналов
MEME_CHANNEL_IDS = [int(os.getenv('MEME1')), int(os.getenv('MEME2'))]
CONSOLE_OUTPUT_CHANNEL_ID = int(os.getenv('CONSOLE_OUTPUT'))
TARGET_GUILD_ID = int(os.getenv('TARGET_GUILD'))

# Эмодзи и шанс реакции
EMOJI_LIST = ["🇮🇱", "🍆"]
REACTION_CHANCE = 0.1  # 10%