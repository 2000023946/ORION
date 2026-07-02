from src.domain.query import Query


def test_query_initialization():
    query = Query("Find all laptops")

    assert query.text == "Find all laptops"


def test_query_allows_empty_string():
    query = Query("")

    assert query.text == ""