# import pytest
# import asyncio

# from src.domain.query import Query
# from src.application.mcp_orchestrator import MCPOrchestrator
# from src.application.graph_executer import GraphExecutor

# from src.application.graph_executer import GraphExecutor
# from src.infrastructure.dummy.dummy_tool_execution_port import DummyToolExecutionPort
# from src.infrastructure.dummy.dummy_llm_port import DummyLLMPort
# from src.infrastructure.dummy.dummy_tool_registry_port import DummyToolRegistryPort


# @pytest.mark.asyncio
# async def test_mcp_orchestrator_end_to_end():

#     orchestrator = MCPOrchestrator(
#         llm_port=DummyLLMPort(),
#         tool_registry_port=DummyToolRegistryPort(),
#         graph_executor=GraphExecutor(
#             tool_execution_port=DummyToolExecutionPort()
#         )
#     )

#     result = await orchestrator.run(Query(text="what is AI?"))

#     # validate final answer
#     assert result.answer is not None
#     assert isinstance(result.sources, list)

#     # ensure system actually ran DAG + synthesis
#     assert "Fake answer" in result.answer or "AI" in result.answer