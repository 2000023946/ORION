# import pytest

# from src.components.app import App
# from src.domain.query import Query
# from src.domain.search_answer import SearchAnswer
# from src.ports.llm_port import LLMPort
# from src.application.graph_executer import GraphExecutor


# # ----------------------------
# # Fake GraphExecutor (sync for testing)
# # ----------------------------
# class FakeGraphExecutor(GraphExecutor):

#     async def execute(self, plan):
#         # simulate tool execution output
#         return {
#             "step1": {"content": "fake tool output", "score": 1.0}
#         }


# # ----------------------------
# # Test 1: App wiring works
# # ----------------------------
# def test_app_initialization():

#     app = App()

#     assert app.orchestrator is not None
#     assert app.llm is not None
#     assert app.tool_registry is not None
#     assert app.graph_executor is not None


# # ----------------------------
# # Test 2: App run returns SearchAnswer
# # ----------------------------
# @pytest.mark.asyncio
# async def test_app_run_returns_search_answer(monkeypatch):

#     app = App()

#     # replace real graph executor with fake one
#     app.graph_executor = FakeGraphExecutor()

#     # monkeypatch LLM methods so we fully control behavior
#     class FakeLLM(LLMPort):

#         def create_plan(self, query, tools):
#             class FakePlan:
#                 steps = [{"tool": "Fake Tool"}]
#             return FakePlan()

#         def synthesize(self, query, results):
#             return SearchAnswer(text="final answer from app")

#     app.llm = FakeLLM()

#     result = await app.run("hello world")

#     assert isinstance(result, SearchAnswer)
#     assert result.text == "final answer from app"


# # ----------------------------
# # Test 3: App converts string → Query correctly
# # ----------------------------
# @pytest.mark.asyncio
# async def test_app_query_conversion(monkeypatch):

#     app = App()

#     class FakeLLM(LLMPort):

#         def create_plan(self, query, tools):
#             assert query.text == "test query"

#             class FakePlan:
#                 steps = []
#             return FakePlan()

#         def synthesize(self, query, results):
#             return SearchAnswer(text="ok")

#     app.llm = FakeLLM()
#     app.graph_executor = FakeGraphExecutor()

#     result = await app.run("test query")

#     assert result.text == "ok"