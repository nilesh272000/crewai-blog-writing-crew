from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from crewai_blog.schemas import BlogRequest, BlogResponse
from crewai_blog.services.blog_service import BlogService

app = FastAPI(
    title="CrewAI Blog Writing Crew",
    version="1.0.0",
    description="Planner → Writer → Editor multi-agent blog generation API.",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
service = BlogService()


@app.get("/")
def home():
    return FileResponse("templates/index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": "crewai-blog-writing-crew"}


@app.post("/api/blog/generate", response_model=BlogResponse)
def generate_blog(request: BlogRequest):
    try:
        return service.generate(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
