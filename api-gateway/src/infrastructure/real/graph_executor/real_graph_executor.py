import asyncio
from collections import deque

from src.domain.context import Context
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.tool_name import ToolName
from src.ports.graph_executer_port import GraphExecutorPort
from src.ports.mcp_server_port import MCPServerPort, ToolResponse


class RealGraphExecuter(GraphExecutorPort):

    async def execute(self, plan: RetrievalPlan, mcp_server: MCPServerPort) -> Context:
        context = Context()

        graph = plan.graph
        visited: set[ToolName] = set()

        # start from sources ONLY (trust the plan)
        queue = deque(plan.sources)

        while queue:

            # ----------------------------
            # 1. build current layer
            # ----------------------------
            layer: list[ToolName] = []

            for _ in range(len(queue)):
                node = queue.popleft()

                if node in visited:
                    continue

                visited.add(node)
                layer.append(node)

            # ----------------------------
            # 2. parallel execution
            # ----------------------------
            await asyncio.gather(
                *[self._run_node(node, mcp_server, context) for node in layer]
            )

            # ----------------------------
            # 3. enqueue next nodes
            # ----------------------------
            for node in layer:
                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        queue.append(neighbor)

        return context

    async def _run_node(
        self, 
        tool_name: ToolName, 
        mcp_server: MCPServerPort, 
        context: Context
    ) -> None:
        response: ToolResponse = await mcp_server.call_tool(tool_name)
        context.update(tool_name, response.output)