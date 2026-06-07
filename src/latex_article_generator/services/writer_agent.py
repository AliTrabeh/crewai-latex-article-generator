"""WriterAgent factory — task 008."""

from crewai import Agent


def build_writer_agent(config: dict) -> Agent:
    """Return a configured WriterAgent."""
    return Agent(
        role="Academic Writer",
        goal=(
            "Draft clear, well-structured academic article sections "
            "based on the provided research brief."
        ),
        backstory=(
            "You are an experienced academic writer skilled in producing "
            "publication-ready prose for computer science and engineering papers."
        ),
        tools=[],
        verbose=config.get("verbose", False),
        allow_delegation=False,
        max_iter=config.get("max_iter", 5),
    )
