from crewai import Agent

from crewai_blog.tools.seo_keyword_tool import SEOKeywordTool


def build_agents():
    seo_tool = SEOKeywordTool()

    planner = Agent(
        role="Content Planner",
        goal="Create a detailed, search-friendly content strategy and outline for the requested topic.",
        backstory=(
            "You are an experienced SEO content strategist. You understand search intent, "
            "reader journeys, information architecture, and technical content structure."
        ),
        tools=[seo_tool],
        verbose=False,
        allow_delegation=False,
    )

    writer = Agent(
        role="Content Writer",
        goal="Write an engaging, useful and well-structured blog post based strictly on the approved outline.",
        backstory=(
            "You are a senior technology writer who explains difficult concepts clearly, "
            "uses practical examples, and writes for modern online readers."
        ),
        verbose=False,
        allow_delegation=False,
    )

    editor = Agent(
        role="Senior Editor",
        goal="Turn the draft into a polished, readable and SEO-friendly final blog post.",
        backstory=(
            "You are an experienced editor focused on clarity, grammar, structure, "
            "reader engagement, consistency and responsible claims."
        ),
        verbose=False,
        allow_delegation=False,
    )

    return planner, writer, editor
