import pytest
import asyncio

from src.application.graph_executer import GraphExecutor
from src.infrastructure.dummy.dummy_tool_execution_port import DummyToolExecutionPort
from src.infrastructure.dummy.dummy_llm_port import DummyLLMPort
from src.domain.query import Query

@pytest.mark.asyncio
async def test_graph_executor_dag_execution():

    llm = DummyLLMPort()
    plan = llm.create_plan(Query(text="AI test"), [])

    executor = GraphExecutor(
        tool_execution_port=DummyToolExecutionPort()
    )

    results = await executor.execute(plan)

    # ensure all nodes executed
    assert "s1" in results
    assert "s2" in results
    assert "s3" in results

    # validate structure
    assert results["s1"]["step_id"] == "s1"
    assert results["s2"]["step_id"] == "s2"
    assert results["s3"]["step_id"] == "s3"