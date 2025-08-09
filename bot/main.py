import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from handlers import commands, background, recommendations

load_dotenv()

bot = Bot(
    token=os.getenv("BOT_TOKEN"),
    parse_mode=ParseMode.HTHTML
)
dp = Dispatcher()


dp.include_router(commands.router)
dp.include_router(background.router)
dp.include_router(recommendations.router)

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я твой персональный ассистент и помогу тебе выбрать магистерскую программу ИТМО.\n\n"
        "Доступные команды:\n"
        "/background - Рассказать о своем опыте\n"
        "/recommend - Получить рекомендации по дисциплинам\n"
        "/compare - Сравнить программы"
    )
@dp.message(Command("compare"))
async def compare_programs(message: Message):
    comparison = (
        "Сравнение программ:\n\n"
        "Искусственный интеллект:\n"
        "- Фокус: алгоритмы, ML, нейросети\n"
        "- Проекты: исследовательские\n"
        "- Карьера: Data Scientist, Researcher\n\n"
        "Управление ИИ-продуктами:\n"
        "- Фокус: продуктовый менеджмент, внедрение AI\n"
        "- Проекты: индустриальные\n"
        "- Карьера: AI Product Manager\n\n"
    )
    await message.answer(comparison)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())