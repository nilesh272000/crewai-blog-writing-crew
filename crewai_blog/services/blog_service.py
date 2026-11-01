import re
from typing import List

from crewai import Crew, Process

from crewai_blog.agents.blog_agents import build_agents
from crewai_blog.config import is_mock_mode
from crewai_blog.schemas import BlogRequest, BlogResponse
from crewai_blog.tasks.blog_tasks import build_tasks


class BlogService:
    def __init__(self):
        self.planner, self.writer, self.editor = build_agents()

    @staticmethod
    def _keywords(request: BlogRequest) -> List[str]:
        if request.keywords:
            return request.keywords
        topic = request.topic.strip()
        return [
            topic.lower(),
            f"{topic.lower()} guide",
            f"{topic.lower()} tutorial",
            f"{topic.lower()} best practices",
        ]

    def _mock_response(self, request: BlogRequest) -> BlogResponse:
        keywords = self._keywords(request)
        title = f"{request.topic}: A Practical Guide for {request.audience.title()}"
        outline = (
            f"# Outline: {title}\n\n"
            "## 1. Introduction\n- Why the topic matters\n- What readers will learn\n\n"
            "## 2. Core Concepts\n- Key terminology\n- How the approach works\n\n"
            "## 3. Practical Implementation\n- Recommended workflow\n- Common design decisions\n\n"
            "## 4. Best Practices\n- Quality, security and maintainability\n\n"
            "## 5. Common Mistakes\n- Pitfalls and how to avoid them\n\n"
            "## 6. FAQ\n- Frequently asked reader questions\n"
        )
        draft = (
            f"# {title}\n\n"
            f"{request.topic} is an important topic for {request.audience}. "
            "A practical approach starts with a clear understanding of the problem, "
            "the intended audience and the desired outcome.\n\n"
            "## Core Concepts\n\n"
            f"The foundation of {request.topic} is to connect the right concepts into a "
            "repeatable workflow. Teams should start with requirements, define measurable "
            "quality criteria and then implement the simplest reliable architecture.\n\n"
            "## Practical Implementation\n\n"
            "Break the solution into small components, validate each stage, and add "
            "observability before scaling. This makes failures easier to diagnose and "
            "future improvements easier to introduce.\n\n"
            "## Best Practices\n\n"
            "Keep the design modular, test important behavior, protect credentials, "
            "and include human review when incorrect output could cause harm.\n"
        )
        final = (
            f"# {title}\n\n"
            f"## Introduction\n\n{request.topic} can be approached as a structured "
            f"problem rather than a single task. For {request.audience}, the goal is to "
            "create a workflow that is useful, understandable and maintainable.\n\n"
            "## Core Concepts\n\n"
            f"A strong implementation begins by defining what {request.topic} should "
            "achieve. Then separate planning, execution and quality review so each "
            "stage has a clear responsibility.\n\n"
            "## Practical Workflow\n\n"
            "1. Define the objective and audience.\n"
            "2. Break the work into focused stages.\n"
            "3. Generate the first version.\n"
            "4. Review quality and correctness.\n"
            "5. Refine and publish only after human validation.\n\n"
            "## Best Practices\n\n"
            "Use modular components, explicit inputs and outputs, logging, tests and "
            "clear failure handling. Avoid unsupported claims and keep sensitive content "
            "under appropriate human review.\n\n"
            "## Common Mistakes\n\n"
            "The most common mistakes are unclear requirements, excessive complexity, "
            "weak evaluation criteria and treating generated text as automatically factual.\n\n"
            "## FAQ\n\n"
            f"### What is the best way to learn {request.topic}?\n\n"
            "Start with the fundamentals, build a small implementation and iterate using "
            "measurable feedback.\n\n"
            "### Is a complex architecture always better?\n\n"
            "No. Prefer the simplest design that meets the reliability and quality goals.\n"
        )
        meta = f"Practical {request.topic} guide for {request.audience}, covering concepts, workflow and best practices."
        return BlogResponse(
            topic=request.topic,
            outline=outline,
            draft=draft,
            final_blog=final,
            seo_keywords=keywords,
            title=title,
            meta_description=meta[:160],
            mode="mock",
            workflow=["Planner Agent", "Writer Agent", "Editor Agent"],
        )

    def generate(self, request: BlogRequest) -> BlogResponse:
        if is_mock_mode():
            return self._mock_response(request)

        inputs = {
            "topic": request.topic,
            "audience": request.audience,
            "tone": request.tone,
            "target_words": request.target_words,
            "keywords": ", ".join(self._keywords(request)),
        }

        planning_task, writing_task, editing_task = build_tasks(
            self.planner, self.writer, self.editor, request
        )

        crew = Crew(
            agents=[self.planner, self.writer, self.editor],
            tasks=[planning_task, writing_task, editing_task],
            process=Process.sequential,
            verbose=False,
        )

        result = crew.kickoff(inputs=inputs)
        outputs = getattr(result, "tasks_output", []) or []

        outline = str(outputs[0].raw) if len(outputs) > 0 else ""
        draft = str(outputs[1].raw) if len(outputs) > 1 else ""
        final_blog = str(outputs[2].raw) if len(outputs) > 2 else str(result)

        title = self._extract_title(final_blog, request.topic)
        keywords = self._keywords(request)
        meta = self._build_meta(final_blog, request)

        return BlogResponse(
            topic=request.topic,
            outline=outline,
            draft=draft,
            final_blog=final_blog,
            seo_keywords=keywords,
            title=title,
            meta_description=meta,
            mode="crewai",
            workflow=["Planner Agent", "Writer Agent", "Editor Agent"],
        )

    @staticmethod
    def _extract_title(text: str, topic: str) -> str:
        match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
        return match.group(1).strip() if match else f"{topic}: A Practical Guide"

    @staticmethod
    def _build_meta(text: str, request: BlogRequest) -> str:
        clean = re.sub(r"[#*_`>\n]+", " ", text)
        clean = re.sub(r"\s+", " ", clean).strip()
        return f"{request.topic}: practical insights, implementation guidance and best practices for {request.audience}."[:160]
