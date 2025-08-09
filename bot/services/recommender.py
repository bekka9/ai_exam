import json
from openai import OpenAI
import os

def load_program_data():
    with open("data/ai_curriculum.json") as f:
        ai_plan = json.load(f)
    with open("data/ai_product.json") as f:
        ai_product_plan = json.load(f)
    return ai_plan, ai_product_plan

def generate_recommendation_prompt(user_data, ai_plan, ai_product_plan):
    return f"""
Ты - консультант по поступлению в университет ИТМО. Помоги абитуриенту выбрать между существующими программами:
1. Искусственный интеллект (AI)
2. Управление ИИ-продуктами (AI Product)
Предложи релевантную программу, которая бы соответствовала увлечениям абитуриента

Данные абитуриента:
- Образование: {user_data.get('education', 'не указано')}
- Опыт: {user_data.get('experience', 'не указан')}
- Интересы: {user_data.get('interests', 'не указаны')}

Учебные планы:
[Программа AI]
{json.dumps(ai_plan, ensure_ascii=False, indent=2)}

[Программа AI Product]
{json.dumps(ai_product_plan, ensure_ascii=False, indent=2)}

Сформируй:
1. рекомендацию по программе 
2. укажии топ-3 выборных дисциплины для каждой программы, котороые подходят больше всего
3. распиши план обучения на 4 семестра с указанием ключевых дисциплин
4. напиши обоснование своего выбора (связь с бэкграундом)

Формат вывода:
Наиболее подходящая вам программа: ... 
Дисциплины, которые были бы вам интересны: дисциплина1, дисциплина2, дисциплина3
План обучения, основываясь на ваших увлечениях:
  • Семестр 1: ...
  • Семестр 2: ...
Почему имеено эта программа: ...
"""

def get_recommendations(user_data: dict):
    ai_plan, ai_product_plan = load_program_data()
    prompt = generate_recommendation_prompt(user_data, ai_plan, ai_product_plan)
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )
    
    return response.choices[0].message.content