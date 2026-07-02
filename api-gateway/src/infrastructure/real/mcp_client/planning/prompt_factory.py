from src.infrastructure.real.mcp_client.planning.create_plan_instruction import CREATE_PLAN_INSTRUCTION
from src.infrastructure.real.mcp_client.planning.prompt import Prompt
from src.domain.context import Context
from src.domain.query import Query
from src.domain.tool import Tool
from src.infrastructure.real.mcp_client.planning.answer_instruction import ANSWER_INSTRUCTION
from src.infrastructure.real.mcp_server.tools.db_filter.db_filter_instruction import DB_FILTER_INSTRUCTION

class PromptFactory:
    
    def get_tool_names(self, tools: list[Tool]) -> list[str]:
        return [t.name.name for t in tools]
    
    def create_plan_prompt(self, query: Query, tools: list[Tool]) -> Prompt:
        tool_names = self.get_tool_names(tools)

        prompt_text = f"""
            {CREATE_PLAN_INSTRUCTION}

            QUERY:
            {query.text}

            AVAILABLE TOOLS:
            {tool_names}

            Return ONLY JSON.
        """

        return Prompt(prompt=prompt_text)
    
    def create_answer_prompt(self, query: Query, context: Context) -> Prompt:

        prompt_text = f"""
            {ANSWER_INSTRUCTION}

            USER QUERY:
            {query.text}

            TOOL RESULTS:
            {context}

            FINAL ANSWER:
            """

        return Prompt(prompt=prompt_text.strip())


    def create_db_filter_prompt(self, query: Query) -> Prompt:

        prompt_text = f"""
            {DB_FILTER_INSTRUCTION}

            USER QUERY:
            {query.text}

            FINAL OUTPUT:
            """.strip()

        return Prompt(prompt=prompt_text)
        