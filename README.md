bot/

├── data/                   # Парсинг и хранение учебных планов

│   ├── ai_curriculum.json  # Учебный план "Искусственный интеллект"

│   └── ai_product.json     # Учебный план "AI Product"

├── scrapers/               

│   └── pdf_parser.py       # Парсинг в JSON

├── bot/                    # Telegram-бот

│   ├── handlers/           # Обработчики команд

│   │   ├── commands.py     # /start, /help

│   │   ├── background.py   # Сбор данных о пользователе

│   │   ├── compare.py      # Сравнение программ

│   │   └── questions.py    # Ответы на вопросы

│   ├── services/           

│   │   ├── parser.py       # Обработка данных

│   │   ├── rag.py          # RAG-система

│   │   └── recommender.py  # Рекомендации

│   └── main.py             # Запуск бота

├── .env                    

├── requirements.txt        
├── Dockerfile              
└── README.md              

