"""ReviewerAgent factory — task 009."""

from crewai import Agent


def build_reviewer_agent(config: dict) -> Agent:
    """Return a configured ReviewerAgent."""
    return Agent(
        role="Academic Reviewer",
        goal=(
            "Review the drafted article sections for academic quality, "
            "logical consistency, completeness, and citation accuracy. "
            "Provide specific, actionable feedback."
        ),
        backstory=(
            "You are a rigorous peer reviewer for top-tier academic conferences, "
            "known for thorough and constructive critique."
        ),
        tools=[],
        verbose=config.get("verbose", False),
        allow_delegation=False,
        max_iter=config.get("max_iter", 3),
    )
