from src.indexer import InvertedIndexer


def test_tokenize_basic():
    indexer = InvertedIndexer()

    words = indexer.tokenize("Hello World!")

    assert words == ["hello", "world"]


def test_tokenize_case_insensitive():
    indexer = InvertedIndexer()

    words = indexer.tokenize("Good GOOD good")

    assert words == ["good", "good", "good"]


def test_add_page_frequency():
    indexer = InvertedIndexer()

    indexer.add_page("page1", "life is life")

    entry = indexer.get_word_entry("life")

    assert entry["page1"]["freq"] == 2


def test_add_page_positions():
    indexer = InvertedIndexer()

    indexer.add_page("page1", "one two one")

    entry = indexer.get_word_entry("one")

    assert entry["page1"]["positions"] == [0, 2]


def test_build_index():
    indexer = InvertedIndexer()

    data = {
        "page1": "hello world",
        "page2": "hello python"
    }

    index = indexer.build_index(data)

    assert "hello" in index
    assert "world" in index
    assert "python" in index