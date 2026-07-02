from src.domain.search_answer import SearchAnswer


def test_search_answer_initialization():
    answer = SearchAnswer("This is the answer.")

    assert answer.answer == "This is the answer."


def test_search_answer_repr():
    answer = SearchAnswer("This is the answer.")

    assert repr(answer) == "SearchAnswer(answer=This is the answer.)"


def test_search_answer_to_dict():
    answer = SearchAnswer("This is the answer.")

    assert answer.to_dict() == {
        "answer": "This is the answer."
    }