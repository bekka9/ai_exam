from aiogram import Router
from aiogram.types import Message
from services.recommender import get_recommendations
import Command
import json
router = Router()

@router.message(Command("recommend"))
async def recommend_courses(message: Message):
    try:
        with open("user_background.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        await message.answer("Сначала расскажи о себе через /background")
        return
    
    recommendations = get_recommendations(user_data)
    await message.answer(recommendations)