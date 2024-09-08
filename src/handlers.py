import os
import json
import aiohttp

from telebot.types import Message

from src.bot import bot


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message: Message):
    await bot.send_message(
        message.chat.id,
        "Здравствуйте, сообщите ваш запрос"
    )


@bot.message_handler(func=(lambda message: True))
async def handler(message: Message):
    data = {
        "text": message.text
    }
    data = json.dumps(data)

    url = os.getenv("URL")

    timeout = aiohttp.ClientTimeout(total=900)
    connector = aiohttp.TCPConnector(limit=600)


    try:
        async with aiohttp.ClientSession(
            timeout=timeout,
            connector=connector
        ) as session:
            async with session.post(
                url,
                data=data,
                timeout=600
            ) as response:
                result: str = json.dumps(
                    await response.json(),
                    indent=2,
                    ensure_ascii=False
                )  # json
                response_to_user = f"```json\n{result}\n```"

                await bot.send_message(
                    message.chat.id,
                    text=response_to_user,
                    parse_mode="MarkdownV2"
                )
    except:
        await bot.send_message(
            message.chat.id,
            text="произошла ошибка, подождите, пожалуйста",
            parse_mode="MarkdownV2"
        )
