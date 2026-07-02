from typing import Any, Sequence
from pymongo import MongoClient
from pymongo.collection import Collection

from src.infrastructure.config.settings import settings


class MongoSeeder:
    def __init__(
        self,
    ) -> None:
        # Use settings as default (clean MCP design)
        self.client: MongoClient[Any] = MongoClient(
            settings.metadata_db_url
        )

        self.db = self.client[
            settings.metadata_db_name
        ]

        self.collection: Collection[dict[str, Any]] = self.db[
            settings.metadata_collection_name
        ]

    def clear(self) -> None:
        """Delete all documents in the collection."""
        self.collection.delete_many({})

    def seed(self, data: Sequence[dict[str, Any]]) -> None:
        """
        Insert seed data into the collection.
        """
        if not data:
            raise ValueError("Seed data is empty")

        self.collection.insert_many(list(data))


    def reset_and_seed(self, data: Sequence[dict[str, Any]]) -> None:
        """
        Full reset + seed (most common dev usage).
        """
        self.clear()
        self.seed(data)
        print(f"Seeded {len(data)} documents into {self.collection.name}")