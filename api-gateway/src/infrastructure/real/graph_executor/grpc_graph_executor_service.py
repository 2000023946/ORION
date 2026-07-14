import asyncio
import json
import grpc
import os
import sys



# Import the auto-generated gRPC code
from src.infrastructure.real.graph_executor import executor_pb2
from src.infrastructure.real.graph_executor import executor_pb2_grpc

# Import your domain models
from src.components.graph_executor_infrastructure import GraphExecutorInfrastructure
from src.components.mcp_server_infrastructure import MCPServerInfrastructure
from src.domain.query import Query
from src.domain.tool_edge import ToolEdge
from src.domain.tool_name import ToolName
from src.domain.retrieval_plan import RetrievalPlan

# Import your real infrastructure
from src.ports.graph_executer_port import GraphExecutorPort
from src.ports.mcp_server_port import MCPServerPort

from enum import Enum


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
        
        # The graph builds itself!
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
            # If the tools crash, tell the Gateway exactly why
            context.abort(grpc.StatusCode.INTERNAL, f"Graph execution failed: {str(e)}")
        # 3. Pack Domain Objects -> Protobuf
        
        # 3. Pack Domain Objects -> Protobuf
        # Ask the Context to give us a perfectly clean, JSON-safe dictionary
        clean_context_dict = final_context.to_dict()
        
        proto_context_data = {
            # Since clean_context_dict already converted ToolName to strings, 
            # we just dump the values straight into the Protobuf map
            tool_name_str: json.dumps(output_value) 
            for tool_name_str, output_value in clean_context_dict.items()
        }

        return executor_pb2.ExecutionResponse(
            context=executor_pb2.Context(data=proto_context_data)
        )


async def serve():
    # 1. Grab your tool registry and factory from your standard config
    from src.components.app import App
    
    app_container = App(mock=True)
    
    # 2. DO NOT use app_container.graph_executor! 
    # That is the gRPC client. We must build the REAL one here.
    real_graph_executor = app_container.graph_executor_infras.real_graph_executor
    mcp_server = app_container.mcp_server_infras.mcp_server
    
    # 3. Pass the REAL executor and the REAL mcp_server into the Servicer
    server = grpc.aio.server()
    executor_pb2_grpc.add_GraphExecutorServiceServicer_to_server(
        GrpcGraphExecutorServicer(real_graph_executor, mcp_server), 
        server
    )
    
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print(f"Executor Microservice starting on {listen_addr}...")
    
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())