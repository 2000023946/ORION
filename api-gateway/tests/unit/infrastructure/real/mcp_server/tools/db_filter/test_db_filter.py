import pytest
from src.infrastructure.real.mcp_server.tools.db_filter.db_filter import DBFilter  # type: ignore



# -------------------------
# create() - full fields
# -------------------------
def test_db_filter_create_full():
    raw = {
        "name": "laptop",
        "min_price": "100",
        "max_price": "500"
    }

    f = DBFilter.create(raw)

    assert f.name == "laptop"
    assert f.min_price == 100.0
    assert f.max_price == 500.0


# -------------------------
# create() - partial fields
# -------------------------
def test_db_filter_create_partial():

    raw = {
        "name": "phone"
    }

    f = DBFilter.create(raw)

    assert f.name == "phone"
    assert f.min_price is None
    assert f.max_price is None


# -------------------------
# get_db_query - name only
# -------------------------
def test_db_filter_query_name_only():

    f = DBFilter(name="shoe")

    query = f.get_db_query()

    assert query == {
        "name": {
            "$regex": "shoe",
            "$options": "i"
        }
    }


# -------------------------
# get_db_query - price only
# -------------------------
def test_db_filter_query_price_only():

    f = DBFilter(min_price=10, max_price=50)

    query = f.get_db_query()

    assert query == {
        "price": {
            "$gte": 10,
            "$lte": 50
        }
    }


# -------------------------
# get_db_query - combined
# -------------------------
def test_db_filter_query_combined():

    f = DBFilter(name="book", min_price=5, max_price=20)

    query = f.get_db_query()

    assert query == {
        "name": {
            "$regex": "book",
            "$options": "i"
        },
        "price": {
            "$gte": 5,
            "$lte": 20
        }
    }


# -------------------------
# get_db_query - empty
# -------------------------
def test_db_filter_query_empty():

    f = DBFilter()

    assert f.get_db_query() == {}