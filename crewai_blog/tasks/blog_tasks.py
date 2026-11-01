from crewai import Task


def build_tasks(planner, writer, editor, request):
    planning_task = Task(
        description=(
            "Create a detailed blog outline for the topic: {topic}. "
            "Audience: {audience}. Tone: {tone}. Target length: {target_words} words. "
            "Requested keywords: {keywords}. "
            "Include search intent, a compelling title idea, H1/H2/H3 structure, "
            "key points per section, examples, FAQs and an SEO keyword plan. "
            "Return only a practical outline and content plan."
        ),
        expected_output="A detailed, logically ordered blog outline with SEO considerations.",
        agent=planner,
    )

    writing_task = Task(
        description=(
            "Write a complete blog post from the planner's outline. "
            "Topic: {topic}. Audience: {audience}. Tone: {tone}. "
            "Target length: {target_words} words. Keywords: {keywords}. "
            "Make the article useful, natural, engaging and technically coherent. "
            "Do not mention that an AI or agent wrote the article. "
            "Use markdown headings and concise paragraphs."
        ),
        expected_output="A complete blog draft in markdown.",
        agent=writer,
        context=[planning_task],
    )

    editing_task = Task(
        description=(
            "Edit the draft produced by the writer. Improve grammar, readability, "
            "flow, headings, keyword placement, repetition and SEO structure. "
            "Preserve useful technical details and avoid unsupported absolute claims. "
            "Return the final polished blog in markdown with a strong title, "
            "clear sections and a concise FAQ section."
        ),
        expected_output="A publication-ready SEO-friendly blog post in markdown.",
        agent=editor,
        context=[writing_task],
        output_file=None,
    )

    return planning_task, writing_task, editing_task
