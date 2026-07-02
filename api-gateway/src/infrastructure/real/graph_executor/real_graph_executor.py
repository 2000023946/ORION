import asyncio
from collections import deque

from src.constants.constants import START_TOOL, END_TOOL
from src.domain.context import Context
from src.domain.query import Query
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_output_registry import ToolOutputRegistry
from src.infrastructure.real.mcp_server.tools.core.tool_request_factory_registry import ToolRequestFactoryRegistry
from src.ports.graph_executer_port import GraphExecutorPort
from src.ports.mcp_server_port import MCPServerPort
from src.ports.tool_response import ToolResponse


class RealGraphExecuter(GraphExecutorPort):

    def __init__(self, tool_request_factory_registry: ToolRequestFactoryRegistry):
        self.tool_request_factory_registry = tool_request_factory_registry

    async def execute(
        self,
        query: Query,
        plan: RetrievalPlan,
        mcp_server: MCPServerPort
    ) -> Context:

        context: Context = Context()
        graph = plan.graph

        visited: set[ToolName] = set()

        queue: deque[ToolName] = deque([START_TOOL])

        tool_output_registry = ToolOutputRegistry(query=query)

        while queue:

            layer: list[ToolName] = []

            # ----------------------------
            # Build current BFS layer
            # ----------------------------
            for _ in range(len(queue)):
                node: ToolName = queue.popleft()

                if node in visited:
                    continue

                visited.add(node)
                layer.append(node)

            # ----------------------------
            # Execute layer in parallel
            # ----------------------------
            await asyncio.gather(
                *[
                    self._run_node(
                        tool_name=node,
                        mcp_server=mcp_server,
                        context=context,
                        tool_output_registry=tool_output_registry,
                    )
                    for node in layer
                ]
            )



            # ----------------------------
            # Enqueue children
            # ----------------------------
            for node in layer:
                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        queue.append(neighbor)

        return context

    # -------------------------------------------------
    # NODE EXECUTION
    # -------------------------------------------------
    async def _run_node(
        self,
        tool_name: ToolName,
        mcp_server: MCPServerPort,
        context: Context,
        tool_output_registry: ToolOutputRegistry,
    ) -> None:
        print(f"Executing Node {tool_name.name}")
        # START node
        if tool_name == START_TOOL:
            context.update(
                START_TOOL,
                tool_output_registry.get(ToolIOKeys.QUERY),
            )
            return

        # END node
        if tool_name == END_TOOL:
            return

        # Create request
        tool_request = self.tool_request_factory_registry.create_request(
            tool_name=tool_name,
            tool_output_registry=tool_output_registry,
        )
        print("tool request", tool_request.params)
        try:
            tool_response = await mcp_server.call_tool(tool_name, tool_request)
            print("tool response", tool_response.output)
        except Exception as e:
            tool_response = ToolResponse(
                tool_name=tool_name,
                output={},
                success=False,
                error=str(e),
            )

        tool_output_registry.save_response(tool_response)
        context.update(tool_name, tool_response.output)
        
        print("updated context: ", context.context)