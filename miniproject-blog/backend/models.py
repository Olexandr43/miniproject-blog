from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    author: str
    date: str

class ArticleSummary(BaseModel):
    id: int
    title: str
    slug: str
    author: str
    date: str
