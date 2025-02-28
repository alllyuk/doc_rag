# RAG для работы с документацией (Docs Assistant)

## Описание проекта
Чат-бот для работы с произвольной документацией, загруженной в сервис пользователем. После загрузки документации возможно задавать вопросы по ней и получать краткое саммари от бота.

## Последовательность действий по запуску сервиса

1. Сохраняем репозиторий локально:
`git clone https://github.com/alllyuk/doc_rag`

2. Устанавливаем зависимости
`pip install -r requirements.txt`

3. Включаем VPN (для запросов в LLM)

4. Получаем API KEY для LLM по [инструкции](https://www.merge.dev/blog/mistral-ai-api-key).\
Создаем файл `.env` в корне репозитория:
```
MISTRAL_API_URL=https://api.mistral.ai/v1
MISTRAL_API_KEY=<your_api_key>
MISTRALAI_API_KEY=<your_api_key>
```

5. Поднимаем milvus
`docker-compose up -d`

6. Запускаем API
`uvicorn main:app --reload`

7. Запускаем интерфейс
`python demo.py`

Сервис будет доступен по адресу, указанному в логах запуска интерфейса

## Кратко о реализации
Проект выполнен с использованием библиотеки langchain и ее компонентов. В качестве базы данных для хранения документации используется Milvus. Из LLM используется Mistral. Фронтенд реализован на Gradio.

## Примеры интерфейса и валидации сервиса
Запуск сервиса
![Внешний вид](images/1.jpg)
Загрузка документа
![Внешний вид](images/2.jpg)
Задание вопроса чат-боту
![Внешний вид](images/3.jpg)
Использование контекста диалога
![Внешний вид](images/4.jpg)
Вопросы на отвлеченную тему
![Внешний вид](images/5.jpg)

## Авторы сервиса
- Зарипов Данис. Разработка взаимодействия с LLM, в том числе эмбеддинги. Реализация фронтенда.
- Корнелюк Алексей. Разработка пайплайна RAG и его компонент (ретривер, реранкер), интеграция частей сервиса.
- Ильяшенко Роман. Разработка API и работы с парсингом файлов. Реализация логического разделения кода в сервисе.
