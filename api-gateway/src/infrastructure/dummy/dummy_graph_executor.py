from src.ports.graph_executer import GraphExecutor
from src.domain.retrieval_plan import RetrievalPlan
from src.ports.mcp_server import MCPServer
from src.domain.context import Context
from src.ports.mcp_server import ToolResponse


class DummyGraphExecuter(GraphExecutor):

    def execute(self, plan: RetrievalPlan, mcp_server: MCPServer) -> Context:
        context = Context()

        # pretend execution order = sources first
        to_visit = list(plan.sources)

        visited = set()

        while to_visit:
            tool_name = to_visit.pop(0)

            if tool_name in visited:
                continue

            visited.add(tool_name)

            # call tool
            response: ToolResponse = mcp_server.call_tool(tool_name)

            # store in context
            context.data[tool_name] = response.output

            # add downstream nodes (if they exist in graph)
            for neighbor in plan.graph.get(tool_name, []):
                if neighbor not in visited:
                    to_visit.append(neighbor)

        return context