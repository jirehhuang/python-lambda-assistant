"""Functions and tools for responding to queries."""

from pathlib import Path

from dotenv import load_dotenv
from jhutils.agent import AssistantFactory

# Load environment variables locally
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


_factory = AssistantFactory()


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
    return _factory.assistant.run(query)
