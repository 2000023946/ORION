

from src.domain.input import Input
from src.domain.output import Output
from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys


VECTOR_SEARCH_TOOL = Tool(
    name=ToolName("VECTOR_SEARCH_TOOL"),
    description=(
        "Performs semantic vector search over the document database. "
        "The user's query is converted into a vector embedding and compared "
        "against precomputed document embeddings to find documents with similar "
        "meaning rather than exact keyword matches. "
        "Use this tool for natural language questions, conceptual searches, "
        "or when the user describes something without knowing the exact title "
        "or wording. "
        "This tool returns only the identifiers of the most semantically relevant "
        "documents along with their ranking. Use the Metadata Filter tool afterward "
        "to retrieve the full document contents."
    ),
    inputs=[
        Input(
            name=ToolIOKeys.QUERY,
            type="str",
            description="The user's natural language search query."
        )
    ],
    outputs=[
        Output(
            name=ToolIOKeys.DOCS_IDS,
            type="list[DocId]",
            description="Identifiers of the documents ranked by semantic similarity to the query."
        )
    ]
)

WEB_SEARCH_TOOL = Tool(
    name=ToolName("WEB_SEARCH_TOOL"),
    description=(
        "Searches the public web for current and external information. "
        "Use this tool whenever the user's request depends on recent events, "
        "live information, news, current prices, up-to-date facts, or knowledge "
        "that is unlikely to exist in the internal document database. "
        "This tool should not be used for retrieving internal documents."
    ),
    inputs=[
        Input(
            name=ToolIOKeys.QUERY,
            type="str",
            description="The user's search query."
        )
    ],
    outputs=[
        Output(
            name=ToolIOKeys.WEB_RESULTS,
            type="WebSearchResponse",
            description="Structured web search results containing relevant webpages and summaries."
        )
    ]
)

DB_FILTER_TOOL = Tool(
    name=ToolName("DB_FILTER_TOOL"),
    description=(
        "Retrieves complete documents given their document identifiers. "
        "This tool performs a direct lookup by document ID and returns the "
        "full stored document information, including title, content, price, "
        "and metadata. "
        "Use this tool after Vector Search when only document IDs are available "
        "and the actual document contents are needed."
    ),
    inputs=[
        Input(
            name=ToolIOKeys.DOCS_IDS,
            type="list[DocId]",
            description="List of document identifiers to retrieve."
        )
    ],
    outputs=[
        Output(
            name=ToolIOKeys.DOCUMENTS,
            type="list[Document]",
            description="The complete documents corresponding to the provided document identifiers."
        )
    ]
)



METADATA_FILTER_TOOL = Tool(
    name=ToolName("METADATA_FILTER_TOOL"),
    description=(
        "Performs structured filtering directly on the document database using "
        "simple database filters. This tool extracts product names and price "
        "constraints from the user's query and filters documents accordingly. "
        "Only the fields 'name', 'min_price', and 'max_price' may be used for "
        "filtering. "
        "Use this tool when the query explicitly mentions a product name, a "
        "price limit, a budget, a minimum price, a maximum price, or a "
        "combination of name and price. "
        "Unlike semantic vector search, this tool performs exact structured "
        "database filtering and returns the matching documents directly."
    ),
    inputs=[
        Input(
            name=ToolIOKeys.QUERY,
            type="str",
            description="The user's query containing optional product name and/or price constraints."
        )
    ],
    outputs=[
        Output(
            name=ToolIOKeys.DOCUMENTS,
            type="list[Document]",
            description="Documents that satisfy the generated database filtering conditions."
        )
    ]
)
