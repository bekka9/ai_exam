from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import Command
import json
router = Router()

class BackgroundState(StatesGroup):
    education = State()
    experience = State()
    interests = State()

@router.message(Command("background"))
async def start_background_collection(message: Message, state: FSMContext):
    await message.answer("Расскажи о своем образовании (вуз, специальность):")
    await state.set_state(BackgroundState.education)

@router.message(BackgroundState.education)
async def process_education(message: Message, state: FSMContext):
    await state.update_data(education=message.text)
    await message.answer("Опиши свой профессиональный опыт:")
    await state.set_state(BackgroundState.experience)

@router.message(BackgroundState.experience)
async def process_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("Какие направления ИИ тебя интересуют?")
    await state.set_state(BackgroundState.interests)

@router.message(BackgroundState.interests)
async def process_interests(message: Message, state: FSMContext):
    await state.update_data(interests=message.text)
    background_data = await state.get_data()
    
    with open("user_background.json", "w") as f:
        json.dump(background_data, f)
    
    await message.answer("Спасибо! Эта информация поможет с рекомендациями")
    await state.clear()