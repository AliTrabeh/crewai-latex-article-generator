"""CrewAI task factories for all four pipeline tasks (tasks 011–014)."""

from crewai import Task


def build_research_task(topic: str, sections: list[str], agent) -> Task:
    """Return the research Task for the given topic."""
    sections_str = ", ".join(sections)
    return Task(
        description=(
            f"Research the topic: '{topic}'.\n"
            f"Focus on these sections: {sections_str}.\n"
            "Gather credible academic sources, key findings, and relevant data. "
            "Produce a structured research brief with source citations."
        ),
        expected_output=(
            "A structured research brief containing:\n"
            "1. Key concepts and definitions\n"
            "2. Current state of the art\n"
            "3. At least 5 cited academic sources (author, title, year, venue)\n"
            "4. Key findings relevant to each requested section"
        ),
        agent=agent,
    )


def build_writing_task(topic: str, sections: list[str], agent, research_task: Task) -> Task:
    """Return the writing Task; depends on research_task for context."""
    sections_str = ", ".join(sections)
    return Task(
        description=(
            f"Write the following sections of an academic article about '{topic}':\n"
            f"{sections_str}\n\n"
            "Use the research brief from the previous task as your source. "
            "Write in clear academic English. Include in-text citations. "
            "If a section requires Hebrew content, write it in Hebrew with proper RTL formatting."
        ),
        expected_output=(
            "Complete prose for each requested section, clearly delimited by section name. "
            "Each section must be at least 300 words. "
            "Citations must be in the format [Author, Year]."
        ),
        agent=agent,
        context=[research_task],
    )


def build_review_task(agent, writing_task: Task) -> Task:
    """Return the review Task; depends on writing_task for context."""
    return Task(
        description=(
            "Review the drafted article sections for:\n"
            "1. Academic quality and clarity\n"
            "2. Logical flow between sections\n"
            "3. Citation accuracy and completeness\n"
            "4. Factual consistency with the research brief\n"
            "5. Correctness of Hebrew/RTL sections (if present)\n\n"
            "Produce an improved, final version of the article with all issues addressed."
        ),
        expected_output=(
            "The final, revised article text with all sections. "
            "Include a brief review summary (max 200 words) at the top noting what was changed."
        ),
        agent=agent,
        context=[writing_task],
    )


def build_formatting_task(agent, review_task: Task) -> Task:
    """Return the formatting Task; depends on review_task for context."""
    return Task(
        description=(
            "Convert the reviewed article text into a complete, compilable LaTeX document.\n"
            "Structure the document with proper LaTeX environments for each section.\n"
            r"Apply RTL formatting (\begin{RTL}...\end{RTL}) for any Hebrew content."
            "\nInclude a full preamble with all required packages."
        ),
        expected_output=(
            r"A complete LaTeX document starting with \documentclass{article}. "
            "The document must be compilable with LuaLaTeX without errors."
        ),
        agent=agent,
        context=[review_task],
    )
