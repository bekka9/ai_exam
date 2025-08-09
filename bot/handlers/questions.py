from aiogram import Router, F
from aiogram.types import Message
from services.rag import answer_question
import re

router = Router()

PROGRAM_NAMES = ["искусственный интеллект", "ai", "продукт", "product"]

@router.message(F.text)
async def handle_question(message: Message):
    if not any(name in message.text.lower() for name in PROGRAM_NAMES):
        await message.answer("Я отвечаю только на вопросы о магистерских программах ИИ и AI Product. Задайте вопрос о программах.")
        return
    response = answer_question(message.text)
    await message.answer(response)