from datetime import datetime, timezone
from typing import Any


SEED_DATA: list[dict[str, Any]] = [
    {
        "_id": "p1",
        "title": "iPhone 15",
        "content": "Latest Apple smartphone with A16 chip",
        "price": 999,
        "metadata": {
            "category": "phone",
            "brand": "Apple",
        },
        "created_at": datetime.now(timezone.utc),
    },
    {
        "_id": "p2",
        "title": "iPhone 14",
        "content": "Previous generation Apple smartphone",
        "price": 799,
        "metadata": {
            "category": "phone",
            "brand": "Apple",
        },
        "created_at": datetime.now(timezone.utc),
    },
    {
        "_id": "p3",
        "title": "Galaxy S24",
        "content": "Samsung flagship Android phone",
        "price": 899,
        "metadata": {
            "category": "phone",
            "brand": "Samsung",
        },
        "created_at": datetime.now(timezone.utc),
    },
    {
        "_id": "p4",
        "title": "Pixel 8",
        "content": "Google AI-powered smartphone",
        "price": 699,
        "metadata": {
            "category": "phone",
            "brand": "Google",
        },
        "created_at": datetime.now(timezone.utc),
    },
    {
        "_id": "p5",
        "title": "MacBook Pro",
        "content": "High performance laptop for professionals",
        "price": 1999,
        "metadata": {
            "category": "laptop",
            "brand": "Apple",
        },
        "created_at": datetime.now(timezone.utc),
    },
    {
        "_id": "p6",
        "title": "MacBook Air",
        "content": "Lightweight Apple laptop",
        "price": 1199,
        "metadata": {
            "category": "laptop",
            "brand": "Apple",
        },
        "created_at": datetime.now(timezone.utc),
    },
    {
        "_id": "p7",
        "title": "Dell XPS 13",
        "content": "Premium Windows ultrabook",
        "price": 1099,
        "metadata": {
            "category": "laptop",
            "brand": "Dell",
        },
        "created_at": datetime.now(timezone.utc),
    },
    {
        "_id": "p8",
        "title": "iPad Pro",
        "content": "Apple tablet for productivity and creativity",
        "price": 1299,
        "metadata": {
            "category": "tablet",
            "brand": "Apple",
        },
        "created_at": datetime.now(timezone.utc),
    },
    {
        "_id": "p9",
        "title": "AirPods Pro",
        "content": "Noise cancelling wireless earbuds",
        "price": 249,
        "metadata": {
            "category": "audio",
            "brand": "Apple",
        },
        "created_at": datetime.now(timezone.utc),
    },
    {
        "_id": "p10",
        "title": "Sony WH-1000XM5",
        "content": "Industry leading noise cancelling headphones",
        "price": 399,
        "metadata": {
            "category": "audio",
            "brand": "Sony",
        },
        "created_at": datetime.now(timezone.utc),
    },
]