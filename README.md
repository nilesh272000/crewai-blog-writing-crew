# CrewAI Blog Writing Crew

Production-oriented multi-agent blog writing system built with **CrewAI + FastAPI + vanilla JavaScript**.

The system follows a clear Planner → Writer → Editor workflow:

```text
User Topic
   ↓
Planner Agent
   ↓
Blog Outline
   ↓
Writer Agent
   ↓
Draft Blog
   ↓
Editor Agent
   ↓
Final SEO-Friendly Blog
```

## Why this project is portfolio-ready

- Multi-agent orchestration with CrewAI
- Specialized Planner, Writer, and Editor agents
- Sequential task execution
- Dynamic topic input
- Custom deterministic SEO keyword tool
- FastAPI backend
- Interactive browser UI
- Structured API request/response models
- Environment-based LLM configuration
- Local demo/mock mode for UI development
- Tests for API contracts and workflow configuration
- Clear separation of agents, tasks, services, schemas, and frontend
- No Docker and no API keys committed

## Tech Stack

- Python 3.10+
- CrewAI
- OpenAI-compatible LLM
- FastAPI
- Pydantic
- Uvicorn
- HTML/CSS/JavaScript
- Pytest

## Project Structure

```text
CrewAI-Blog-Writing-Crew-Portfolio/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
├── crewai_blog/
│   ├── __init__.py
│   ├── config.py
│   ├── crew.py
│   ├── schemas.py
│   ├── workflow.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── blog_agents.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── blog_tasks.py
│   ├── tools/
│   │   ├── __init__.py
│   │   └── seo_keyword_tool.py
│   └── services/
│       ├── __init__.py
│       └── blog_service.py
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
├── data/
│   └── sample_topics.json
├── docs/
│   └── architecture.md
└── tests/
    ├── test_api.py
    ├── test_schemas.py
    └── test_workflow_config.py
```

## Setup

### 1. Create virtual environment

Windows:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```cmd
pip install -r requirements.txt
```

### 3. Configure environment

Copy:

```text
.env.example → .env
```

Set:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
MOCK_MODE=false
```

For UI/API development without an LLM key:

```env
MOCK_MODE=true
```

## Run

```cmd
python -m uvicorn app:app --reload --port 8080
```

Open:

```text
http://127.0.0.1:8080
```

Swagger:

```text
http://127.0.0.1:8080/docs
```

Health:

```text
http://127.0.0.1:8080/health
```

## API

### Generate blog

`POST /api/blog/generate`

Example:

```json
{
  "topic": "Agentic AI",
  "audience": "AI engineers",
  "tone": "professional",
  "target_words": 1200,
  "keywords": ["agentic AI", "LangGraph", "LLM agents"]
}
```

The response contains:

- outline
- draft
- final blog
- generated metadata
- keyword suggestions
- execution information

## Crew Design

### Planner Agent

Role: Content Planner

Responsibilities:

- understand the topic
- identify audience intent
- build a logical outline
- include SEO considerations
- define headings and content flow

### Writer Agent

Role: Content Writer

Responsibilities:

- transform the outline into a detailed article
- maintain readability
- use examples
- follow the target audience and tone
- naturally incorporate keywords

### Editor Agent

Role: Senior Editor

Responsibilities:

- improve grammar
- remove repetition
- improve readability
- strengthen SEO structure
- preserve factual caution
- return a polished final article

## Interview Explanation

> "I designed the application as a sequential CrewAI workflow. A Planner agent first creates the content strategy and outline. A Writer agent consumes that output and produces the article. An Editor agent then reviews and improves the draft for grammar, readability and SEO. The workflow is exposed through FastAPI and a browser UI, while agent definitions, tasks, tools and services are kept modular for maintainability."

## Portfolio Talking Points

- Why multi-agent instead of one prompt?
  - Each agent has a focused responsibility, making the workflow easier to control, test and extend.
- Why sequential process?
  - Each stage depends on the previous stage's output, so sequential execution matches the dependency graph.
- How would you scale it?
  - Add parallel research agents, persistent job state, async workers, observability, caching, evaluation and a vector database.
- How would you evaluate quality?
  - SEO score, readability, factuality, keyword coverage, citation correctness and human evaluation.
- How would you add RAG?
  - Add a research/retrieval agent before writing and pass grounded sources into the writer/editor context.
- How would you add human-in-the-loop?
  - Pause after planning or editing and require approval before the next task.

## Safety / Quality

This is a content-generation demo. It should not be used as an autonomous publishing system without human review, especially for medical, financial, legal, or other high-impact content.

## License

MIT.
