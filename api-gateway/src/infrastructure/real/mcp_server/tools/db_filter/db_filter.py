from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class DBFilter:
    name: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

    # ----------------------------
    # Factory: from raw LLM output
    # ----------------------------
    @classmethod
    def create(cls, raw: dict[str, Any]) -> "DBFilter":


        name = raw.get("name", None)

        min_price = raw.get("min", None)
        max_price = raw.get("max", None)

        return cls(
            name=name,
            min_price=float(min_price) if min_price is not None else None,
            max_price=float(max_price) if max_price is not None else None
        )
        
    def get_db_query(self) -> dict[str, Any]:
        db_query_payload: dict[str, Any] = {
            "name": self.name,
            "min_price": self.min_price,
            "max_price": self.max_price
        }
        db_query_payload = {k: v for k, v in db_query_payload.items() if v is not None}
        
        return db_query_payload