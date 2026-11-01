from crewai_blog.schemas import BlogRequest


def test_blog_request_defaults():
    request = BlogRequest(topic="Agentic AI")
    assert request.audience == "technology professionals"
    assert request.target_words == 1200


def test_blog_request_keywords():
    request = BlogRequest(topic="RAG", keywords=["RAG", "vector database"])
    assert len(request.keywords) == 2
