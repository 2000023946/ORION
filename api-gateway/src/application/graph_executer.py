import asyncio
from collections import defaultdict, deque
from src.ports.tool_execution_port import ToolExecutionPort
from src.domain.retrieval_plan import RetrievalPlan


class GraphExecutor:
    def __init__(self, tool_execution_port: ToolExecutionPort):
        self.tool_execution_port = tool_execution_port

    async def execute(self, plan: RetrievalPlan):
        steps = plan.steps
        edges = plan.edges

        # build graph
        graph = defaultdict(list)
        indegree = defaultdict(int)

        for frm, to in edges:
            graph[frm].append(to)
            indegree[to] += 1

        # find starting nodes (no dependencies)
        queue = deque([s_id for s_id in steps if indegree[s_id] == 0])

        results = {}

        while queue:
            batch = []

            # collect all currently runnable nodes
            for _ in range(len(queue)):
                batch.append(queue.popleft())

            # run batch in parallel
            tasks = [
                self.tool_execution_port.execute(steps[step_id])
                for step_id in batch
            ]

            outputs = await asyncio.gather(*tasks)

            # store results
            for step_id, output in zip(batch, outputs):
                results[step_id] = output

                # unlock children
                for neighbor in graph[step_id]:
                    indegree[neighbor] -= 1
                    if indegree[neighbor] == 0:
                        queue.append(neighbor)

        return results