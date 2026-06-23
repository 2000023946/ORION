from src.domain.retrieval_step import RetrievalStep
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.search_answer import SearchAnswer


class DummyLLMPort:
    def create_plan(self, query, tools):
        # simple fake DAG plan

        step1 = RetrievalStep(
            step_id="s1",
            type="semantic_search",
            input=query.text,
            params={"top_k": 3},
            depends_on=[]
        )

        step2 = RetrievalStep(
            step_id="s2",
            type="web_search",
            input=query.text,
            params={},
            depends_on=[]
        )

        step3 = RetrievalStep(
            step_id="s3",
            type="merge",
            input="s1+s2",
            params={},
            depends_on=["s1", "s2"]
        )

        steps = {
            "s1": step1,
            "s2": step2,
            "s3": step3
        }

        edges = [
            ("s1", "s3"),
            ("s2", "s3")
        ]

        return RetrievalPlan(query=query.text, steps=steps, edges=edges)

    def synthesize(self, query, results):
        return SearchAnswer(
            answer=f"Fake answer for: {query.text}",
            sources=[str(r) for r in results]
        )