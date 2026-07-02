from src.domain.input import Input
from src.domain.output import Output
from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys


VECTOR_SEARCH_TOOL = Tool(
    name=ToolName("VECTOR_SEARCH_TOOL"),
    description=(
        "PRIMARY RETRIEVAL TOOL (MANDATORY FORMAT CONTRACT)\n\n"
        "PURPOSE:\n"
        "- Converts a natural language query into semantic document IDs using vector search.\n\n"
        "INPUT RULES:\n"
        "- MUST receive: query: str\n"
        "- Query must be raw user text (no transformations required)\n\n"
        "OUTPUT RULES:\n"
        "- ONLY returns: docs_ids: list[DocId]\n"
        "- Output MUST NOT contain documents, text, or metadata\n"
        "- Output MUST be used by METADATA_FILTER_TOOL if present\n\n"
        "EXECUTION RULE:\n"
        "- Can ONLY be executed directly from START\n"
        "- Must appear in any valid retrieval path involving semantic search\n\n"
        "HARD CONSTRAINT:\n"
        "- If query is missing → tool fails\n"
        "- If output is not docs_ids → invalid execution\n"
    ),
    inputs=[
        Input(
            name=ToolIOKeys.QUERY,
            type="str",
            description="Raw user query. Required for execution.",
        )
    ],
    outputs=[
        Output(
            name=ToolIOKeys.DOCS_IDS,
            type="list[DocId]",
            description="ONLY document IDs. Required for downstream filtering.",
        )
    ],
)


WEB_SEARCH_TOOL = Tool(
    name=ToolName("WEB_SEARCH_TOOL"),
    description=(
        "EXTERNAL KNOWLEDGE RETRIEVAL TOOL (REAL-TIME INFORMATION)\n\n"
        "PURPOSE:\n"
        "- Fetches up-to-date external information from the web.\n\n"
        "WHEN TO USE:\n"
        "- MUST be used for: recent events, news, releases, live information\n"
        "- SHOULD be preferred when query contains: 'latest', 'new', 'today', 'release', 'update'\n\n"
        "INPUT RULES:\n"
        "- Requires: query: str\n\n"
        "OUTPUT RULES:\n"
        "- Returns: results: WebSearchResponse\n"
        "- Output is independent (does NOT feed other tools unless explicitly required)\n\n"
        "EXECUTION RULE:\n"
        "- Always callable from START\n"
        "- Cannot depend on other tools\n\n"
        "HARD CONSTRAINT:\n"
        "- If query is unrelated to external info → tool should not be selected by planner\n"
    ),
    inputs=[
        Input(
            name=ToolIOKeys.QUERY,
            type="str",
            description="Search query for web retrieval.",
        )
    ],
    outputs=[
        Output(
            name=ToolIOKeys.WEB_RESULTS,
            type="WebSearchResponse",
            description="External web search results.",
        )
    ],
)
DB_FILTER_TOOL = Tool(
    name=ToolName("DB_FILTER_TOOL"),
    description=(
        "STRUCTURED DATABASE FILTER TOOL (STRICT QUERY ENGINE)\n\n"
        "PURPOSE:\n"
        "- Translates user query into structured database filters (Mongo-style)\n"
        "- Performs exact or range-based filtering (name, price, category)\n\n"
        "INPUT RULES:\n"
        "- Requires query: str (MANDATORY)\n"
        "- Query MUST be structured or semi-structured intent\n\n"
        "OUTPUT RULES:\n"
        "- Returns: documents: list[Document]\n"
        "- Output is FINAL database result (no further processing required)\n\n"
        "EXECUTION RULE:\n"
        "- Can be called directly from START\n"
        "- Does NOT require VECTOR_SEARCH_TOOL\n\n"
        "IMPORTANT BEHAVIOR:\n"
        "- This tool bypasses semantic search completely\n"
        "- It is independent of METADATA_FILTER_TOOL\n\n"
        "HARD CONSTRAINT:\n"
        "- If query cannot be parsed into DB filters → tool may return empty result\n"
    ),
    inputs=[
        Input(
            name=ToolIOKeys.QUERY,
            type="str",
            description="Structured or semi-structured query for DB filtering.",
        ),
    ],
    outputs=[
        Output(
            name=ToolIOKeys.DOCUMENTS,
            type="list[Document]",
            description="Filtered database documents.",
        )
    ],
)

METADATA_FILTER_TOOL = Tool(
    name=ToolName("METADATA_FILTER_TOOL"),
    description=(
        "POST-PROCESSING FILTER (STRICT DEPENDENCY TOOL)\n\n"
        "PURPOSE:\n"
        "- Refines results from VECTOR_SEARCH_TOOL using document metadata\n\n"
        "INPUT RULES (STRICT):\n"
        "- REQUIRED input: docs_ids: list[DocId]\n"
        "- docs_ids MUST come ONLY from VECTOR_SEARCH_TOOL\n"
        "- If docs_ids is missing → tool is INVALID\n\n"
        "OUTPUT RULES:\n"
        "- Returns: documents: list[Document]\n"
        "- Output is refined subset of vector search results\n\n"
        "DEPENDENCY RULE (CRITICAL):\n"
        "- MUST ONLY execute AFTER VECTOR_SEARCH_TOOL\n"
        "- MUST NEVER be connected directly from START\n"
        "- MUST NOT appear without VECTOR_SEARCH_TOOL upstream\n\n"
        "EXECUTION RULE:\n"
        "- This tool is NEVER independent\n"
        "- It always depends on semantic retrieval first\n\n"
        "HARD CONSTRAINT:\n"
        "- If docs_ids is empty → execution MUST fail\n"
        "- If no VECTOR_SEARCH_TOOL in path → invalid DAG\n"
    ),
    inputs=[
        Input(
            name=ToolIOKeys.DOCS_IDS,
            type="list[DocId]",
            description="ONLY valid output from VECTOR_SEARCH_TOOL.",
        )
    ],
    outputs=[
        Output(
            name=ToolIOKeys.DOCUMENTS,
            type="list[Document]",
            description="Filtered and ranked documents after metadata refinement.",
        )
    ],
)