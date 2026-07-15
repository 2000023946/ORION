import json
import grpc

# Import the generated gRPC files
import src.infrastructure.real.graph_executor.executor_pb2 as executor_pb2
import src.infrastructure.real.graph_executor.executor_pb2_grpc as executor_pb2_grpc

# Import your domain models
from src.domain.context import Context
from src.domain.query import Query
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.tool_name import ToolName
from src.ports.graph_executer_port import GraphExecutorPort
from src.ports.mcp_server_port import MCPServerPort


class GrpcGraphExecutor(GraphExecutorPort):
    def __init__(self, target_address: str):
        self.target_address = target_address

    async def execute(
        self,
        query: Query,
        plan: RetrievalPlan,
        mcp_server: MCPServerPort
    ) -> Context:
        # Note: We ignore mcp_server here because the Gateway no longer runs the tools!
        # The tools now live entirely inside the new Executor Service.
        
        # 1. Open an asynchronous connection to the Executor Microservice
        async with grpc.aio.insecure_channel(self.target_address) as channel:
            stub = executor_pb2_grpc.GraphExecutorServiceStub(channel)

            # 2. Pack Domain Objects -> Protobuf
            proto_edges = [
                executor_pb2.ToolEdge(source=edge.source.name, to=edge.to.name)
                for edge in plan.edges
            ]
            proto_plan = executor_pb2.RetrievalPlan(edges=proto_edges)

            request = executor_pb2.ExecutionRequest(
                query_text=query.text,
                plan=proto_plan
            )

            # 3. Fire the network request!
            try:
                response = await stub.ExecutePlan(request)
            except grpc.RpcError as e:
                raise RuntimeError(f"Failed to communicate with Graph Executor Service: {e.details()}")

            # 4. Unpack Protobuf -> Domain Objects
            final_context_dict = {}
            for tool_name_str, json_data_str in response.context.data.items():
                # Parse the JSON string back into a Python dict/object
                final_context_dict[ToolName(tool_name_str)] = json.loads(json_data_str)

            return Context(context=final_context_dict)