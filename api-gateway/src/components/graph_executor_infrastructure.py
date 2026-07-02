from src.infrastructure.real.graph_executor.real_graph_executor import RealGraphExecuter
from src.infrastructure.real.mcp_server.tools.core.docs_ids_request_factory import DocsIdsRequestFactory
from src.infrastructure.real.mcp_server.tools.core.query_request_factory import QueryRequestFactory
from src.infrastructure.real.mcp_server.tools.core.tool_information import DB_FILTER_TOOL, METADATA_FILTER_TOOL, VECTOR_SEARCH_TOOL, WEB_SEARCH_TOOL
from src.infrastructure.real.mcp_server.tools.core.tool_request_factory_registry import ToolRequestFactoryRegistry


class GraphExecutorInfrastructure:
    def __init__(self):
        # INIT REQUEST FACTORIES
        search_request_factory = QueryRequestFactory()
        docs_ids_request_factory = DocsIdsRequestFactory()
        
        # REGISTER THE REQUESTS FACTORIES UNDER THE TOOLS
        request_registery = ToolRequestFactoryRegistry()
        request_registery.register_factory(VECTOR_SEARCH_TOOL.name, search_request_factory)
        request_registery.register_factory(WEB_SEARCH_TOOL.name, search_request_factory)
        request_registery.register_factory(DB_FILTER_TOOL.name, search_request_factory)
        request_registery.register_factory(METADATA_FILTER_TOOL.name, docs_ids_request_factory)
        
        self.graph_executor = RealGraphExecuter(request_registery)