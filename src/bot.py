# bot.py
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import logging

API_TOKEN = '8107235811:AAGl4_MHhgHQMF89SXVvU4CC7iNQZ7CdCEk'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработка команд
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Привет! Отправь мне данные в формате CSV")

# Обработка документов
@dp.message()
async def handle_docs(message: Message):
    if message.document and message.document.mime_type == 'text/csv':
        await message.document.download()
        await message.answer("Файл получен! Обрабатываю...")
        # Здесь добавить обработку файла
    else:
        await message.answer("Отправьте CSV файл")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())