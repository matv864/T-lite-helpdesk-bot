import json
import aiohttp

from telebot.types import Message

from src.bot import bot

URL = "http://176.123.161.1:8000/assist"


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message: Message):
    await bot.send_message(
        message.chat.id,
        "Здравствуйте, сообщите ваш запрос"
    )


@bot.message_handler(func=(lambda message: True))
async def handler(message: Message):
    data = {
        "query": message.text
    }
    data = json.dumps(data)
    # создали все нужные данные для запроса

    timeout = aiohttp.ClientTimeout(total=900)
    connector = aiohttp.TCPConnector(limit=600)
    # создали инструменты, которые укажут на длительное ожидание ответа

    try:
        async with aiohttp.ClientSession(
            timeout=timeout,
            connector=connector
        ) as session:
            # создали сессию
            async with session.post(
                URL,
                data=data,
                timeout=600
            ) as response:
                # создали запрос
                result: str = json.dumps(
                    await response.json(),
                    indent=2,
                    ensure_ascii=False
                )  # json
                # получили ответ и сделали из него красивый json

                response_to_user = f"```json\n{result}\n```"
                # сделали обёртку для Markdown и красоты сообщения

                # отправляем сообщение пользователю
                await bot.send_message(
                    message.chat.id,
                    text=response_to_user,
                    parse_mode="MarkdownV2"
                )
    except Exception:
        await bot.send_message(
            message.chat.id,
            text="произошла ошибка, подождите, пожалуйста",
            parse_mode="MarkdownV2"
        )
