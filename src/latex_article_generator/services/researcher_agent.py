"""ResearcherAgent factory — task 007."""

from crewai import LLM, Agent


def build_researcher_agent(config: dict) -> Agent:
    """Return a configured ResearcherAgent."""
    return Agent(
        role="Academic Researcher",
        goal=(
            "Thoroughly investigate the given topic and gather credible, "
            "up-to-date academic and technical sources."
        ),
        backstory=(
            "You are a meticulous academic researcher with expertise in "
            "literature review, source verification, and structured knowledge synthesis."
        ),
        llm=LLM(model="anthropic/claude-sonnet-4-6"),
        tools=[],
        verbose=config.get("verbose", False),
        allow_delegation=False,
        max_iter=config.get("max_iter", 5),
    )
