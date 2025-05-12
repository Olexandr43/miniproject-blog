from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import List
from .models import Article, ArticleSummary
from .github_api import create_github_file

app = FastAPI(
    title="Блог API",
    description="API для простого блогу зі статтями. Дозволяє отримувати список статей та окремі статті.",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "Articles",
            "description": "Операції зі статтями",
        }
    ]
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500",
    "https://miniproject-blog.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "backend/db.json"

def load_articles_from_db() -> List[Article]:
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            articles_data = json.load(f)
            return [Article(**article) for article in articles_data]
    except FileNotFoundError:
        print(f"Error: Файл {DB_FILE} не знайдено.")
        return []
    except json.JSONDecodeError:
        print(f"Error: {DB_FILE} містить некоректний JSON.")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

@app.get("/api/articles", response_model=List[ArticleSummary], tags=["Articles"], summary="Отримати список всіх статей")
async def get_articles():
    articles = load_articles_from_db()
    print(f"Завантажені статті: {articles}")
    return [ArticleSummary(id=article.id, title=article.title, slug=article.slug, author=article.author, date=article.date) for article in articles]

@app.get("/api/articles/{article_slug}", response_model=Article, tags=["Articles"], summary="Отримати статтю за її slug")
async def get_article(article_slug: str):
    articles = load_articles_from_db()
    print(f"Шукаємо статтю з slug: {article_slug}")
    for article in articles:
        print(f"Знайдена стаття: {article.slug}")
        if article.slug == article_slug:
            return article
    raise HTTPException(status_code=404, detail="Статтю не знайдено")

def transliterate(text: str) -> str:
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ye',
        'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l',
        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'yu',
        'я': 'ya'
    }
    return ''.join(translit_dict.get(char, char) for char in text.lower())

@app.post("/api/articles", response_model=Article, tags=["Articles"], summary="Створити нову статтю")
async def create_article(article: Article):
    try:
        article.slug = transliterate(article.title)
        articles = load_articles_from_db()
        articles.append(article)
        content = json.dumps([article.dict() for article in articles], ensure_ascii=False, indent=4)
        create_github_file('Olexandr43/miniproject-blog', f'backend/db.json', content)
        return article
    except Exception as e:
        print(f"Помилка при створенні статті: {e}")
        raise HTTPException(status_code=500, detail="Не вдалося створити статтю")

@app.delete("/api/articles/{article_id}", tags=["Articles"], summary="Видалити статтю")
async def delete_article(article_id: int):
    articles = load_articles_from_db()
    for article in articles:
        if article.id == article_id:
            articles.remove(article)
            save_articles_to_db(articles)
            return {"detail": "Статтю видалено"}
    raise HTTPException(status_code=404, detail="Статтю не знайдено")

def save_articles_to_db(articles: List[Article]):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump([article.dict() for article in articles], f, ensure_ascii=False, indent=4)

@app.post("/api/github/create-file")
async def create_file(repo: str, path: str, content: str):
    return create_github_file(repo, path, content)
