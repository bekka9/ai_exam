# bot/handlers/compare.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
import json

router = Router()


def load_programs_data():
    with open("data/ai_curriculum.json", encoding="utf-8") as f:
        ai_data = json.load(f)
    with open("data/ai_product.json", encoding="utf-8") as f:
        ai_product_data = json.load(f)
    return ai_data, ai_product_data

@router.message(Command("compare"))
async def cmd_compare(message: Message):
    ai_data, ai_product_data = load_programs_data()
    
    builder = InlineKeyboardBuilder()
    builder.button(text="По семестрам", callback_data="compare_by_semester")
    builder.button(text=" Для кого", callback_data="compare_for_who")
    builder.button(text="Основные дисциплины", callback_data="compare_main_courses")
    builder.button(text=" Все различия", callback_data="compare_full")
    builder.adjust(2)
    
    comparison_text = """
 <b>Сравнение магистерских программ</b>

<b> Искусственный интеллект (AI)</b>
• Научно-исследовательская направленность
• Упор на алгоритмы и модели ML
• {ai_mandatory} обязательных дисциплин
• {ai_elective} выборных курсов

<b>Управление ИИ-продуктами (AI Product)</b>
• Продуктовая и бизнес-ориентация
• Акцент на внедрение ИИ-решений
• {product_mandatory} обязательных дисциплин
• {product_elective} выборных курсов

Выберите критерий для детального сравнения:
""".format(
        ai_mandatory=ai_data["statistics"]["mandatory_count"],
        ai_elective=ai_data["statistics"]["elective_count"],
        product_mandatory=ai_product_data["statistics"]["mandatory_count"],
        product_elective=ai_product_data["statistics"]["elective_count"]
    )
    
    await message.answer(
        comparison_text,
        reply_markup=builder.as_markup(),
        parse_mode=ParseMode.HTML
    )

@router.callback_query(F.data == "compare_by_semester")
async def compare_by_semester(callback: CallbackQuery):
    ai_data, ai_product_data = load_programs_data()
    
    response = ["<b>Сравнение по семестрам</b>\n"]
    
    for sem in range(1, 5):
        ai_sem = next(s for s in ai_data["semesters"] if s["semester"] == f"Семестр {sem}")
        product_sem = next(s for s in ai_product_data["semesters"] if s["semester"] == f"Семестр {sem}")
        
        response.append(
            f"\n<b>Семестр {sem}:</b>\n"
            f"• <i>AI:</i> {len(ai_sem['mandatory'])} обяз., {len(ai_sem['elective'])} выбор.\n"
            f"• <i>Product:</i> {len(product_sem['mandatory'])} обяз., {len(product_sem['elective'])} выбор."
        )
    
    await callback.message.edit_text(
        "\n".join(response),
        parse_mode=ParseMode.HTML
    )

@router.callback_query(F.data == "compare_for_who")
async def compare_for_who(callback: CallbackQuery):
    text = """
<b>Для кого подходит программа?</b>

<b>Искусственный интеллект:</b>
• Выпускники технических специальностей
• Те, кто хочет углубиться в алгоритмы ИИ
• Будущие исследователи и data scientists
• Разработчики сложных ML-моделей

<b>Управление ИИ-продуктами:</b>
• Выпускники технических и экономических направлений
• Будущие product-менеджеры в ИИ
• Специалисты по внедрению AI-решений
• Те, кто хочет работать на стыке технологий и бизнеса
"""
    await callback.message.edit_text(text, parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "compare_main_courses")
async def compare_main_courses(callback: CallbackQuery):
    ai_data, ai_product_data = load_programs_data()
    
    ai_courses = "\n• ".join(
        d["name"] for s in ai_data["semesters"] 
        for d in s["mandatory"][:3]  # Берем по 3 дисциплины из каждого семестра
    )
    
    product_courses = "\n• ".join(
        d["name"] for s in ai_product_data["semesters"] 
        for d in s["mandatory"][:3]
    )
    
    text = f"""
<b>Ключевые дисциплины программ</b>

<b>Искусственный интеллект:</b>
• {ai_courses}

<b>Управление ИИ-продуктами:</b>
• {product_courses}
"""
    await callback.message.edit_text(text, parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "compare_full")
async def compare_full(callback: CallbackQuery):
    ai_data, ai_product_data = load_programs_data()
    
    stats = {
        "AI": {
            "mandatory": ai_data["statistics"]["mandatory_count"],
            "elective": ai_data["statistics"]["elective_count"],
            "total_hours": sum(
                int(d["workload_hours"]) 
                for s in ai_data["semesters"] 
                for d in s["mandatory"] + s["elective"]
            )
        },
        "Product": {
            "mandatory": ai_product_data["statistics"]["mandatory_count"],
            "elective": ai_product_data["statistics"]["elective_count"],
            "total_hours": sum(
                int(d["workload_hours"]) 
                for s in ai_product_data["semesters"] 
                for d in s["mandatory"] + s["elective"]
            )
        }
    }
    
    text = f"""
<b>Полное сравнение программ</b>

<b> Искусственный интеллект:</b>
• Обязательные дисциплины: {stats['AI']['mandatory']}
• Выборные курсы: {stats['AI']['elective']}
• Общая нагрузка: ~{stats['AI']['total_hours']} часов

<b>Управление ИИ-продуктами:</b>
• Обязательные дисциплины: {stats['Product']['mandatory']}
• Выборные курсы: {stats['Product']['elective']}
• Общая нагрузка: ~{stats['Product']['total_hours']} часов

<b>Основные различия:</b>
• AI фокусируется на разработке алгоритмов
• Product делает акцент на управлении продуктом
• В AI больше математических дисциплин
• В Product больше менеджерских курсов
"""
    await callback.message.edit_text(text, parse_mode=ParseMode.HTML)