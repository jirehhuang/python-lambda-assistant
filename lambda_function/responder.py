"""Functions and tools for responding to queries."""

import os
from pathlib import Path

import instructor
import jhutils
import openai
from dotenv import load_dotenv
from jhutils.agent import AssistantAgent

# Load environment variables locally
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def _initialize_assistant(bool_prod: bool = True) -> AssistantAgent:
    """Initialize the assistant agent."""
    openrouter_client = instructor.from_openai(
        openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
    )

    mealie = jhutils.Mealie(
        api_url=os.getenv("MEALIE_API_URL", ""),
        api_key=os.getenv("MEALIE_API_KEY", ""),
    )

    branch = (
        os.getenv("OBSIDIAN_VAULT_BRANCH_PROD")
        if bool_prod
        else os.getenv("OBSIDIAN_VAULT_BRANCH")
    )
    obsidian = jhutils.Obsidian(
        owner=os.getenv("OBSIDIAN_VAULT_OWNER", ""),
        repository=os.getenv("OBSIDIAN_VAULT_REPOSITORY", ""),
        branch=branch or "",
        github_token=os.getenv("OBSIDIAN_VAULT_TOKEN", ""),
    )

    assistant = AssistantAgent(
        client=openrouter_client, mealie=mealie, obsidian=obsidian
    )
    return assistant


_assistant: AssistantAgent | None = None


def _get_assistant(bool_prod: bool = True) -> AssistantAgent:
    """Lazily initialize and return the assistant agent."""
    # ruff: noqa: PLW0603
    global _assistant  # pylint: disable=global-statement
    if _assistant is None:
        _assistant = _initialize_assistant(bool_prod=bool_prod)
    return _assistant


def respond(query: str) -> str:
    """Respond to user query using assistant agent.

    Parameters
    ----------
    query
        The user query.

    Returns
    -------
    str
        The response from the assistant agent.
    """
    return _get_assistant().run(query)
