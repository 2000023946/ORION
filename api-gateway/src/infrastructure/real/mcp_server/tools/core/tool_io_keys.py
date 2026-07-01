from enum import Enum


class ToolIOKeys(Enum):
    QUERY = "query"
    WEB_RESULTS = "results"
    DOCUMENTS = "documents"
    METADATA = "metadata"
    DOCS_IDS = 'docs_ids'