# Architecture

## High-Level Flow

```text
                  ┌──────────────────┐
                  │   Browser UI     │
                  │ HTML/CSS/JS      │
                  └────────┬─────────┘
                           │ POST /api/blog/generate
                           ▼
                  ┌──────────────────┐
                  │    FastAPI       │
                  │ API + Validation │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │   BlogService    │
                  │ orchestration    │
                  └────────┬─────────┘
                           ▼
                 ┌────────────────────┐
                 │     CrewAI Crew    │
                 │ Process.sequential │
                 └─────────┬──────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        ┌────────┐    ┌────────┐    ┌────────┐
        │Planner │ -> │ Writer │ -> │ Editor │
        │ Agent  │    │ Agent  │    │ Agent  │
        └────────┘    └────────┘    └────────┘
             │             │             │
             ▼             ▼             ▼
          Outline         Draft       Final Blog
```

## Design Principles

1. **Single responsibility per agent**
   - Planner: strategy and outline
   - Writer: content generation
   - Editor: quality improvement

2. **Explicit task dependencies**
   - Writing consumes planning output.
   - Editing consumes writing output.

3. **API/UI separation**
   - FastAPI exposes stable endpoints.
   - Static frontend consumes JSON.

4. **Configuration outside source code**
   - API keys and model names come from `.env`.

5. **Demo-safe development**
   - `MOCK_MODE=true` allows frontend/API testing without an LLM key.

## Production Upgrade Path

- Add a research agent with web search.
- Add RAG for company/product knowledge.
- Add citation verification.
- Add Langfuse/LangSmith-style observability.
- Persist workflow state in PostgreSQL/Redis.
- Run long jobs asynchronously through a queue.
- Add human approval before publishing.
- Add automated SEO/readability/factuality evaluation.
