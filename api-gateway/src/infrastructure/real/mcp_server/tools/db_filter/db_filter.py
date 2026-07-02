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

        min_price = raw.get("min_price", None)
        max_price = raw.get("max_price", None)

        return cls(
            name=name,
            min_price=float(min_price) if min_price is not None else None,
            max_price=float(max_price) if max_price is not None else None
        )
        
    def get_db_query(self) -> dict[str, Any]:
        query: dict[str, Any] = {}

        # -----------------------
        # NAME (case-insensitive contains)
        # -----------------------
        if self.name:
            query["name"] = {
                "$regex": self.name,
                "$options": "i"  # case-insensitive
            }

        # -----------------------
        # PRICE RANGE
        # -----------------------
        price_filter: dict[str, Any] = {}

        if self.min_price is not None:
            price_filter["$gte"] = self.min_price

        if self.max_price is not None:
            price_filter["$lte"] = self.max_price

        if price_filter:
            query["price"] = price_filter

        return query