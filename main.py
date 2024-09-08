import asyncio
from dotenv import load_dotenv

from src.bot import bot
from src.handlers import send_welcome, handler  # noqa

load_dotenv()

asyncio.run(bot.polling())
