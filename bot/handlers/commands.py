from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = """
 <b>Привет, будущий магистрант ИТМО!</b>

Я помогу тебе разобраться в магистерских программах:
• <b>Искусственный интеллект</b> (AI)
• <b>Управление ИИ-продуктами</b> (AI Product)

<b>Доступные команды:</b>
/background - Рассказать о своем опыте
/recommend - Получить персональные рекомендации
/compare - Сравнить программы
/help - Справка по использованию бота

Просто напиши вопрос о программах, например:
"Какие обязательные предметы в AI Product?"
"Чем отличается программа AI от AI Product?"
"""
    await message.answer(welcome_text, parse_mode=ParseMode.HTML)

@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = """
<b>Справка по использованию бота</b>

 <b>Сбор информации о вас:</b>
/background - расскажите о своем образовании, опыте и интересах

 <b>Рекомендации:</b>
/recommend - персонализированные рекомендации по программам
/compare - сравнение двух программ

<b>Работа с данными:</b>
Просто задайте вопрос о программах в свободной форме, например:
• "Какие математические дисциплины есть в AI?"
• "Сколько всего кредитов в AI Product?"
• "Какие языки программирования используются?"

Бот отвечает только на вопросы, связанные с магистерскими программами ИТМО.
"""
    await message.answer(help_text, parse_mode=ParseMode.HTML)

@router.message(Command("about"))
async def cmd_about(message: Message):
    about_text = """
<b>О боте</b>

Этот чат-бот создан для помощи абитуриентам магистратуры ИТМО по направлениям:
• <a href="https://abit.itmo.ru/program/master/ai">Искусственный интеллект</a>
• <a href="https://abit.itmo.ru/program/master/ai_product">Управление ИИ-продуктами</a>

 <b>Функционал:</b>
• Анализ учебных планов
• Персональные рекомендации
• Сравнение программ
• Ответы на вопросы о программах

"""
    await message.answer(about_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

@router.message(F.text == "Привет")
async def handle_hello(message: Message):
    await message.answer("Привет! Чем могу помочь? Используй /help для списка команд.")