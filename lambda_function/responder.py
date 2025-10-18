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


class AssistantManager:
    """Manager class for initializing and accessing the assistant agent."""

    def __init__(self):
        """Initialize the manager with production mode flag."""
        alias = os.getenv("ALIAS", "prod")
        self._bool_prod = alias == "prod"
        self._client: instructor.Instructor | None = None
        self._mealie: jhutils.Mealie | None = None
        self._obsidian: jhutils.Obsidian | None = None
        self._assistant: AssistantAgent | None = None

    @property
    def client(self) -> instructor.Instructor:
        """Get the OpenAI client used by the assistant agent."""
        if self._client is None:
            self._client = instructor.from_openai(
                openai.OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=os.getenv("OPENROUTER_API_KEY"),
                )
            )
        return self._client

    @property
    def mealie(self) -> jhutils.Mealie:
        """Get the Mealie integration used by the assistant agent."""
        if self._mealie is None:
            self._mealie = jhutils.Mealie(
                api_url=os.getenv("MEALIE_API_URL", ""),
                api_key=os.getenv("MEALIE_API_KEY", ""),
            )
        return self._mealie

    @property
    def obsidian(self) -> jhutils.Obsidian:
        """Get the Obsidian integration used by the assistant agent."""
        if self._obsidian is None:
            self._obsidian = jhutils.Obsidian(
                owner=os.getenv("OBSIDIAN_VAULT_OWNER", ""),
                repository=os.getenv("OBSIDIAN_VAULT_REPOSITORY", ""),
                branch="main" if self._bool_prod else "test",
                github_token=os.getenv("OBSIDIAN_VAULT_TOKEN", ""),
            )
        return self._obsidian

    @property
    def assistant(self) -> AssistantAgent:
        """Get the assistant agent."""
        if self._assistant is None:
            self._assistant = AssistantAgent(
                client=self.client, mealie=self.mealie, obsidian=self.obsidian
            )
        return self._assistant


_manager = AssistantManager()


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
    return _manager.assistant.run(query)
