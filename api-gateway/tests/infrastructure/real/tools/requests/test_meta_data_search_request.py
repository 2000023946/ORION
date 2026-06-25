import pytest

from src.domain.retrieval_step import RetrievalStep
from src.infrastructure.real.tools.requests.meta_data_search_request import MetadataRequest


def test_metadata_request_from_retrieval_step_success():

    step = RetrievalStep(
        step_id="1",
        type="metadata",
        input="ignored",
        params={
            "ids": ["doc1", "doc2", "doc3"]
        }
    )

    request = MetadataRequest.from_retrieval_step(step)

    assert request.ids == ["doc1", "doc2", "doc3"]
    assert request.params["ids"] == ["doc1", "doc2", "doc3"]


def test_metadata_request_invalid_step_type():

    step = RetrievalStep(
        step_id="1",
        type="web_search",
        input="ignored",
        params={"ids": ["doc1"]}
    )

    with pytest.raises(ValueError) as e:
        MetadataRequest.from_retrieval_step(step)

    assert "Expected step type 'metadata'" in str(e.value)


def test_metadata_request_missing_ids():

    step = RetrievalStep(
        step_id="1",
        type="metadata",
        input="ignored",
        params={}
    )

    with pytest.raises(ValueError) as e:
        MetadataRequest.from_retrieval_step(step)

    assert "requires 'ids'" in str(e.value)


def test_metadata_request_to_dict():

    step = RetrievalStep(
        step_id="1",
        type="metadata",
        input="ignored",
        params={"ids": ["a", "b"]}
    )

    request = MetadataRequest.from_retrieval_step(step)

    result = request.to_dict()

    assert result == {
        "ids": ["a", "b"],
        "params": {"ids": ["a", "b"]}
    }