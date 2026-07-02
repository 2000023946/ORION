from abc import ABC, abstractmethod
from typing import List

from src.domain.query import Query
from src.domain.context import Context
from src.domain.tool import Tool
from src.infrastructure.real.mcp_client.planning.prompt import Prompt


class PromptFactoryPort(ABC):

    @abstractmethod
    def create_plan_prompt(self, query: Query, tools: List[Tool]) -> Prompt:
        """
        Builds a planning prompt that instructs the LLM to choose tools and produce a plan.
        """
        pass

    @abstractmethod
    def create_answer_prompt(self, query: Query, context: Context) -> Prompt:
        """
        Builds the final answer prompt using tool execution results and context.
        """
        pass

    @abstractmethod
    def create_db_filter_prompt(self, query: Query) -> Prompt:
        """
        Builds a DB filtering instruction prompt (used for structured query filtering).
        """
        pass