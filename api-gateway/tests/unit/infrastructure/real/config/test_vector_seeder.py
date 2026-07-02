from unittest.mock import MagicMock

from src.infrastructure.config.vector_seeder import VectorSeeder



def test_vector_seeder_reset_and_seed():
    # -----------------------
    # mocks
    # -----------------------
    mock_store = MagicMock()
    mock_embedder = MagicMock()

    mock_embedder.embed.side_effect = lambda text: [float(len(text))]

    seeder = VectorSeeder(
        vector_store=mock_store,
        embedder=mock_embedder
    )

    # -----------------------
    # input data
    # -----------------------
    data = [
        {
            "_id": "1",
            "title": "hello",
            "content": "world"
        },
        {
            "_id": "2",
            "title": "foo",
            "content": "bar"
        }
    ]

    # -----------------------
    # execute
    # -----------------------
    seeder.reset_and_seed(data)

    # -----------------------
    # assertions
    # -----------------------

    # reset called once
    mock_store.reset.assert_called_once()

    # embed called for each item
    assert mock_embedder.embed.call_count == 2

    # check correct text formation
    mock_embedder.embed.assert_any_call("hello world")
    mock_embedder.embed.assert_any_call("foo bar")

    # batch insert called correctly
    mock_store.add_batch.assert_called_once()

    args, kwargs = mock_store.add_batch.call_args

    doc_ids, vectors = args

    assert doc_ids == ["1", "2"]
    assert vectors == [[float(len("hello world"))], [float(len("foo bar"))]]