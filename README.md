# Мініпроєкт: Блог зі статтями

Простий блог, розроблений з використанням Python (FastAPI) для backend та статичного HTML/CSS/JS для frontend.

## Опис

Цей проєкт реалізує базовий функціонал блогу:
* Відображення списку статей на головній сторінці.
* Перегляд окремої статті на її власній сторінці.
* Дані про статті зберігаються у JSON файлі.

## Технології

* **Backend:** Python, FastAPI
* **Frontend:** HTML, CSS, JavaScript (Fetch API)
* **База даних:** JSON файл (`db.json`)
* **Управління версіями:** Git
* **Документація API:** Swagger UI / OpenAPI (автоматично генерується FastAPI)
* **Хостинг (планується):** Vercel

## Структура проєкту

```
miniproject-blog/
├── backend/
│   ├── main.py         # Головний файл FastAPI додатку
│   ├── db.json         # База даних статей
│   └── models.py       # Pydantic моделі
├── frontend/
│   ├── index.html      # Головна сторінка (список статей)
│   ├── article.html    # Сторінка перегляду статті
│   ├── css/
│   │   └── style.css   # Стилі
│   └── js/
│       ├── main.js     # JS для index.html
│       └── article.js  # JS для article.html
├── .gitignore          # Файл для ігнорування Git
└── README.md           # Цей файл
```

## Запуск проєкту локально

### Backend

1.  Переконайтесь, що у вас встановлено Python 3.7+ та pip.
2.  Встановіть необхідні бібліотеки:
    ```bash
    pip install fastapi uvicorn "pydantic[email]"
    ```
3.  Перейдіть до директорії `backend`:
    ```bash
    cd backend
    ```
4.  Запустіть FastAPI сервер:
    ```bash
    uvicorn main:app --reload
    ```
    Сервер буде доступний за адресою `http://127.0.0.1:8000`.
    Документація Swagger UI: `http://127.0.0.1:8000/docs`
    Документація ReDoc: `http://127.0.0.1:8000/redoc`

### Frontend

1.  Відкрийте файл `frontend/index.html` у вашому браузері.
    * Найпростіший спосіб - просто клацнути правою кнопкою миші на файлі та вибрати "Open with Live Server" (якщо у вас є відповідне розширення у VS Code) або просто відкрити файл у браузері.
    * **Важливо:** Переконайтесь, що backend сервер запущено, оскільки frontend робить до нього запити.
    * У файлах `frontend/js/main.js` та `frontend/js/article.js` змінна `apiUrl` налаштована на `http://127.0.0.1:8000`. Якщо ваш backend працює на іншому порту чи адресі, змініть це.

## Розгортання на Vercel

* **Backend (FastAPI):**
    * Для розгортання FastAPI на Vercel, потрібно буде створити файл `vercel.json` у корені проєкту для налаштування serverless функцій.
    * Приклад `vercel.json` для FastAPI:
        ```json
        {
          "version": 2,
          "builds": [
            {
              "src": "backend/main.py",
              "use": "@vercel/python"
            }
          ],
          "routes": [
            {
              "src": "/(.*)",
              "dest": "backend/main.py"
            }
          ]
        }
        ```

* **Frontend (Статичний сайт):**
    * Vercel автоматично розпізнає статичні сайти (HTML, CSS, JS).
    * Вам потрібно буде вказати Vercel кореневу директорію для frontend (ймовірно, `frontend`) та команду для збірки (якщо є, в нашому випадку немає).

## Учасники та ролі

* **Backend розробка (FastAPI), Frontend розробка (HTML/CSS/JS):** Василенко Олександр 1к-23 + Cursor/Gemini2.5pro
* **Управління репозиторієм, документація (Swagger/OpenAPI, README.md), розгортання на Vercel:** Василенко Олександр 1к-23

## Swagger/OpenAPI Документація

Після запуску backend сервера, документація API автоматично генерується і доступна за наступними адресами:
* **Swagger UI:** `/docs`
* **ReDoc:** `/redoc`
