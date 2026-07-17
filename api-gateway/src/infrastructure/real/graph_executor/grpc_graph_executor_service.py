import asyncio
import json
import grpc


# 1. Import Prometheus client tools
from prometheus_client import start_http_server

# Import the auto-generated gRPC code
from src.infrastructure.real.graph_executor import executor_pb2
from src.infrastructure.real.graph_executor import executor_pb2_grpc

from src.domain.query import Query
from src.domain.tool_edge import ToolEdge
from src.domain.tool_name import ToolName
from src.domain.retrieval_plan import RetrievalPlan

# Import real infrastructure ports
from src.ports.graph_executer_port import GraphExecutorPort
from src.ports.mcp_server_port import MCPServerPort


class GrpcGraphExecutorServicer(executor_pb2_grpc.GraphExecutorServiceServicer):
    def __init__(self, real_executor: GraphExecutorPort, mcp_server: MCPServerPort):
        self.real_executor = real_executor
        self.mcp_server = mcp_server

    async def ExecutePlan(self, request, context):
        # 1. Unpack Protobuf -> Domain Objects
        domain_edges = [
            ToolEdge(source=ToolName(edge.source), to=ToolName(edge.to))
            for edge in request.plan.edges
        ]
        
        domain_plan = RetrievalPlan(edges=domain_edges)
        domain_query = Query(text=request.query_text)
        
        # 2. Execute the actual graph
        try:
            final_context = await self.real_executor.execute(
                query=domain_query,
                plan=domain_plan,
                mcp_server=self.mcp_server
            )
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, f"Graph execution failed: {str(e)}")
            
        # 3. Pack Domain Objects -> Protobuf
        clean_context_dict = final_context.to_dict()
        
        proto_context_data = {
            tool_name_str: json.dumps(output_value) 
            for tool_name_str, output_value in clean_context_dict.items()
        }

        return executor_pb2.ExecutionResponse(
            context=executor_pb2.Context(data=proto_context_data)
        )


async def serve():
    # 3. Start the standalone background Prometheus HTTP server on port 8000
    # This runs on its own background thread to answer scrape requests from K8s
    metrics_port = 8000
    start_http_server(metrics_port, addr="0.0.0.0")

    # 4. Initialize real infrastructure containers
    from src.components.app import App
    app_container = App(mock=True)
    
    real_graph_executor = app_container.graph_executor_infras.real_graph_executor
    mcp_server = app_container.mcp_server_infras.mcp_server
    
    # 5. Build and bind the gRPC server
    server = grpc.aio.server()
    executor_pb2_grpc.add_GraphExecutorServiceServicer_to_server(
        GrpcGraphExecutorServicer(real_graph_executor, mcp_server), 
        server
    )
    
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())