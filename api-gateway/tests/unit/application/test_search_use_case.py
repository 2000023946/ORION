import pytest  # type: ignore
from unittest.mock import AsyncMock

from src.application.search_response import SearchResponse
from src.application.search_use_case import SearchUseCase
from src.domain.query import Query
from src.domain.search_answer import SearchAnswer
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.context import Context
from src.domain.tool import Tool
from src.domain.tool_name import ToolName


# -------------------------
# helper
# -------------------------
def build_mocks():
    mcp_client = AsyncMock()
    mcp_server = AsyncMock()
    graph_executor = AsyncMock()
    return mcp_client, mcp_server, graph_executor


# -------------------------
# SUCCESS PATH
# -------------------------
@pytest.mark.asyncio  # type: ignore
async def test_search_use_case_success():

    mcp_client, mcp_server, graph_executor = build_mocks()

    query = Query("hello")

    tools = [Tool(ToolName("A"), "desc", [], [])]
    plan = RetrievalPlan([])
    context = Context()
    answer = SearchAnswer("final answer")

    mcp_server.get_tools.return_value = tools
    mcp_client.create_plan.return_value = plan
    graph_executor.execute.return_value = context
    mcp_client.answer.return_value = answer

    use_case = SearchUseCase(
        mcp_client=mcp_client,
        mcp_server=mcp_server,
        graph_executor=graph_executor
    )

    result = await use_case.run(query)

    assert isinstance(result, SearchResponse)
    assert result.success is True
    assert result.answer == answer
    assert result.error is None

    mcp_server.get_tools.assert_awaited_once()
    mcp_client.create_plan.assert_awaited_once_with(query, tools)
    graph_executor.execute.assert_awaited_once_with(query, plan, mcp_server)
    mcp_client.answer.assert_awaited_once_with(query=query, context=context)


# -------------------------
# FAILURE: get_tools
# -------------------------
@pytest.mark.asyncio  # type: ignore
async def test_failure_get_tools():

    mcp_client, mcp_server, graph_executor = build_mocks()

    mcp_server.get_tools.side_effect = Exception("tools failed")

    use_case = SearchUseCase(mcp_client, mcp_server, graph_executor)

    result = await use_case.run(Query("hello"))
    

    assert result.success is False
    assert result.answer is None
    assert result.error is not None


# -------------------------
# FAILURE: create_plan
# -------------------------
@pytest.mark.asyncio  # type: ignore
async def test_failure_create_plan():

    mcp_client, mcp_server, graph_executor = build_mocks()

    mcp_server.get_tools.return_value = []
    mcp_client.create_plan.side_effect = Exception("plan failed")

    use_case = SearchUseCase(mcp_client, mcp_server, graph_executor)

    result = await use_case.run(Query("hello"))

    assert result.success is False
    assert result.answer is None
    assert result.error is not None


# -------------------------
# FAILURE: execute graph
# -------------------------
@pytest.mark.asyncio  # type: ignore
async def test_failure_execute():

    mcp_client, mcp_server, graph_executor = build_mocks()

    mcp_server.get_tools.return_value = []
    mcp_client.create_plan.return_value = RetrievalPlan([])
    graph_executor.execute.side_effect = Exception("execution failed")

    use_case = SearchUseCase(mcp_client, mcp_server, graph_executor)

    result = await use_case.run(Query("hello"))

    assert result.success is False
    assert result.answer is None
    assert result.error is not None


# -------------------------
# FAILURE: answer synthesis
# -------------------------
@pytest.mark.asyncio  # type: ignore
async def test_failure_answer():

    mcp_client, mcp_server, graph_executor = build_mocks()

    mcp_server.get_tools.return_value = []
    mcp_client.create_plan.return_value = RetrievalPlan([])
    graph_executor.execute.return_value = Context()
    mcp_client.answer.side_effect = Exception("llm failed")

    use_case = SearchUseCase(mcp_client, mcp_server, graph_executor)

    result = await use_case.run(Query("hello"))

    assert result.success is False
    assert result.answer is None
    assert result.error is not None


# -------------------------
# CALL ORDER / PIPELINE CHECK
# -------------------------
@pytest.mark.asyncio  # type: ignore
async def test_search_use_case_call_order():

    mcp_client, mcp_server, graph_executor = build_mocks()

    query = Query("hello")

    tools = []
    plan = RetrievalPlan([])
    context = Context()
    answer = SearchAnswer("ok")

    mcp_server.get_tools.return_value = tools
    mcp_client.create_plan.return_value = plan
    graph_executor.execute.return_value = context
    mcp_client.answer.return_value = answer

    use_case = SearchUseCase(mcp_client, mcp_server, graph_executor)

    await use_case.run(query)

    mcp_server.get_tools.assert_awaited_once()
    mcp_client.create_plan.assert_awaited_once()
    graph_executor.execute.assert_awaited_once()
    mcp_client.answer.assert_awaited_once()