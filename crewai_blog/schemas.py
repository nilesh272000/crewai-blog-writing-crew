from typing import List
from pydantic import BaseModel, Field


class BlogRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=200)
    audience: str = Field(default="technology professionals", max_length=120)
    tone: str = Field(default="professional", max_length=60)
    target_words: int = Field(default=1200, ge=400, le=5000)
    keywords: List[str] = Field(default_factory=list, max_length=15)


class BlogResponse(BaseModel):
    topic: str
    outline: str
    draft: str
    final_blog: str
    seo_keywords: List[str]
    title: str
    meta_description: str
    mode: str
    workflow: List[str]
