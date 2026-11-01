from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class SEOKeywordInput(BaseModel):
    topic: str = Field(description="The main blog topic.")


class SEOKeywordTool(BaseTool):
    name: str = "seo_keyword_planner"
    description: str = (
        "Generates a small deterministic list of SEO keyword ideas from a topic. "
        "Use it during content planning."
    )
    args_schema: type[BaseModel] = SEOKeywordInput

    def _run(self, topic: str) -> str:
        cleaned = " ".join(topic.strip().split())
        base = cleaned.lower()
        return (
            f"Primary keyword: {base}\n"
            f"Secondary keywords: {base} guide, {base} tutorial, "
            f"{base} best practices, {base} examples, {base} implementation\n"
            f"Long-tail keyword: how to use {base}"
        )
