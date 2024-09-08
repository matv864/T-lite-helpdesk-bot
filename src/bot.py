import os

from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(os.getenv("BOT_TOKEN"))
