from src.domain.input import Input
from src.domain.output import Output
from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys


VECTOR_SEARCH_TOOL = Tool(
    name=ToolName("VECTOR_SEARCH_TOOL"),
    description=(
        "Performs semantic vector search over the document database.\n\n"
        "INPUT:\n"
        "- query: str (required)\n\n"
        "OUTPUT:\n"
        "- docs_ids: list[DocId] (required)\n\n"
        "CONTRACT:\n"
        "- Requires a query string.\n"
        "- Produces ONLY document IDs.\n"
        "- These IDs are REQUIRED for DB_FILTER_TOOL.\n"
        "- Can run directly from START.\n"
    ),
    inputs=[
        Input(
            name=ToolIOKeys.QUERY,
            type="str",
            description="Natural language query.",
        )
    ],
    outputs=[
        Output(
            name=ToolIOKeys.DOCS_IDS,
            type="list[DocId]",
            description="Ranked document IDs from semantic search.",
        )
    ],
)


WEB_SEARCH_TOOL = Tool(
    name=ToolName("WEB_SEARCH_TOOL"),
    description=(
        "Searches the public web for external and up-to-date information.\n\n"
        "INPUT:\n"
        "- query: str (required)\n\n"
        "OUTPUT:\n"
        "- results: WebSearchResponse\n\n"
        "CONTRACT:\n"
        "- Independent tool.\n"
        "- Always callable from START.\n"
    ),
    inputs=[
        Input(
            name=ToolIOKeys.QUERY,
            type="str",
            description="Search query.",
        )
    ],
    outputs=[
        Output(
            name=ToolIOKeys.WEB_RESULTS,
            type="WebSearchResponse",
            description="Web search results.",
        )
    ],
)


DB_FILTER_TOOL = Tool(
    name=ToolName("DB_FILTER_TOOL"),
    description=(
        "Retrieves and filters full documents using document IDs AND structured constraints.\n\n"
        "INPUT:\n"
        "- docs_ids: list[DocId] (required)\n"
        "- query: str (optional structured filters like name, min_price, max_price)\n\n"
        "OUTPUT:\n"
        "- documents: list[Document]\n\n"
        "CONTRACT (IMPORTANT):\n"
        "- MUST receive docs_ids from VECTOR_SEARCH_TOOL.\n"
        "- Can optionally apply structured filtering (name, price range).\n"
        "- Without docs_ids, this tool WILL FAIL.\n"
    ),
    inputs=[
        Input(
            name=ToolIOKeys.DOCS_IDS,
            type="list[DocId]",
            description="Document IDs from vector search.",
        ),
        Input(
            name=ToolIOKeys.QUERY,
            type="str",
            description="Optional structured filters (name, price range).",
        ),
    ],
    outputs=[
        Output(
            name=ToolIOKeys.DOCUMENTS,
            type="list[Document]",
            description="Final filtered documents.",
        )
    ],
)


METADATA_FILTER_TOOL = Tool(
    name=ToolName("METADATA_FILTER_TOOL"),
    description=(
        "Post-processing metadata filter applied AFTER VECTOR_SEARCH_TOOL.\n\n"
        "INPUT:\n"
        "- docs_ids: list[DocId] (required)\n"
        "- query: str (optional)\n\n"
        "OUTPUT:\n"
        "- documents: list[Document]\n\n"
        "CONTRACT (VERY IMPORTANT):\n"
        "- MUST ONLY run after VECTOR_SEARCH_TOOL.\n"
        "- Requires docs_ids.\n"
        "- Applies lightweight filtering or ranking using metadata.\n"
        "- NOT an independent retrieval tool.\n"
        "- If docs_ids are missing, this tool FAILS.\n"
    ),
    inputs=[
        Input(
            name=ToolIOKeys.DOCS_IDS,
            type="list[DocId]",
            description="Required vector search output.",
        ),
        Input(
            name=ToolIOKeys.QUERY,
            type="str",
            description="Optional metadata refinement query.",
        ),
    ],
    outputs=[
        Output(
            name=ToolIOKeys.DOCUMENTS,
            type="list[Document]",
            description="Refined documents after metadata filtering.",
        )
    ],
)