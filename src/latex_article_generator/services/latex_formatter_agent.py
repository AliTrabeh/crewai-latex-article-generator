"""LaTeXFormatterAgent factory — task 010."""

from crewai import LLM, Agent


def build_latex_formatter_agent(config: dict) -> Agent:
    """Return a configured LaTeXFormatterAgent."""
    return Agent(
        role="LaTeX Formatter",
        goal=(
            "Convert the reviewed article content into syntactically correct LaTeX markup. "
            "Apply proper document structure, section commands, citation commands, "
            "and BiDi directives for Hebrew text."
        ),
        backstory=(
            "You are an expert LaTeX typesetter with deep knowledge of academic paper "
            "formatting, BibTeX/biber citation management, and bidirectional text handling "
            "with polyglossia and bidi packages."
        ),
        llm=LLM(model="anthropic/claude-sonnet-4-6"),
        tools=[],
        verbose=config.get("verbose", False),
        allow_delegation=False,
        max_iter=config.get("max_iter", 5),
    )
