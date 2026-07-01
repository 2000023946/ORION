from dataclasses import dataclass


@dataclass(frozen=True)  
class DocId:
    doc_id: str