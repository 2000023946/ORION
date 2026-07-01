import asyncio
from collections import deque


from src.constants.constants import START_TOOL
from src.domain.context import Context
from src.domain.query import Query
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_inputs import ToolInputs
from src.infrastructure.real.mcp_server.tools.core.tool_output_registry import ToolOutputRegistry
from src.infrastructure.real.mcp_server.tools.core.tool_request_factory_registry import ToolRequestFactoryRegistry
from src.ports.graph_executer_port import GraphExecutorPort
from src.ports.mcp_server_port import MCPServerPort
from src.ports.tool_response import ToolResponse


class RealGraphExecuter(GraphExecutorPort):
    
    def __init__(self, tool_request_factory_registry: ToolRequestFactoryRegistry):
        self.tool_request_factory_registry = tool_request_factory_registry

    async def execute(self, query: Query, plan: RetrievalPlan, mcp_server: MCPServerPort) -> Context:
        context = Context()

        graph = plan.graph
        visited: set[ToolName] = set()

        # FIX: correct deque init
        queue = deque([START_TOOL])

        # registry holds all tool outputs
        tool_output_registry = ToolOutputRegistry(query=query)  # START will seed it below

        while queue:

            layer: list[ToolName] = []

            # ----------------------------
            # 1. build current layer
            # ----------------------------
            for _ in range(len(queue)):
                node = queue.popleft()

                if node in visited:
                    continue

                visited.add(node)
                layer.append(node)

            # ----------------------------
            # 2. execute layer in parallel
            # ----------------------------
            await asyncio.gather(
                *[
                    self._run_node(
                        tool_name=node,
                        mcp_server=mcp_server,
                        context=context,
                        tool_output_registry=tool_output_registry
                    )
                    for node in layer
                ]
            )

            # ----------------------------
            # 3. enqueue children
            # ----------------------------
            for node in layer:
                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        queue.append(neighbor)

        return context

    # -------------------------------------------------
    # CORE NODE EXECUTION FLOW (YOUR REQUIRED ALGORITHM)
    # -------------------------------------------------
    async def _run_node(
        self,
        tool_name: ToolName,
        mcp_server: MCPServerPort,
        context: Context,
        tool_output_registry: ToolOutputRegistry
    ) -> None:

        # ----------------------------
        # 0. START NODE SPECIAL CASE
        # ----------------------------
        if tool_name == START_TOOL:
            # seed context + registry
            context.update(START_TOOL, tool_output_registry.get(ToolInputs.query))
            return

        # ----------------------------
        # 1. CREATE TOOL REQUEST (from registry)
        # ----------------------------
        factory_registry = self.tool_request_factory_registry

        tool_request = factory_registry.create_request(
            tool_name=tool_name,
            tool_output_registry=tool_output_registry
        )

        # ----------------------------
        # 2. BUILD TOOL RESPONSE (pre-execution object)
        # ----------------------------
        tool_response = ToolResponse(
            tool_name=tool_name,
            output={},
            success=True
        )

        try:
            # ----------------------------
            # 3. EXECUTE TOOL
            # ----------------------------
            tool_response = await mcp_server.call_tool(tool_name, tool_request)


        except Exception as e:
            tool_response.success = False
            tool_response.error = str(e)

        # ----------------------------
        # 4. SAVE INTO REGISTRY (IMPORTANT STEP)
        # ----------------------------
        tool_output_registry.save_response(tool_response)

        # ----------------------------
        # 5. UPDATE GLOBAL CONTEXT
        # ----------------------------
        context.update(tool_name, tool_response.output)