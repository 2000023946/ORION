from src.ports.graph_executer_port import GraphExecutorPort
from src.domain.retrieval_plan import RetrievalPlan
from src.ports.mcp_server_port import MCPServerPort
from src.domain.context import Context
from src.ports.mcp_server_port import ToolResponse


class DummyGraphExecuter(GraphExecutorPort):

    async def execute(self, plan: RetrievalPlan, mcp_server: MCPServerPort) -> Context:
        context = Context(context={})

        to_visit = list(plan.sources)
        visited = set()

        while to_visit:
            tool_name = to_visit.pop(0)

            if tool_name in visited:
                continue

            visited.add(tool_name)

            # call tool
            response: ToolResponse = await mcp_server.call_tool(tool_name)

            # store output in context (FIXED)
            context.context[tool_name] = response.output

            # add downstream nodes
            for neighbor in plan.graph.get(tool_name, []):
                if neighbor not in visited:
                    to_visit.append(neighbor)

        return context