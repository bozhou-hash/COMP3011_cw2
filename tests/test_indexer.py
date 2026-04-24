from src.indexer import InvertedIndexer


def test_tokenize_basic():
    indexer = InvertedIndexer()

    words = indexer.tokenize("Hello World!")

    assert words == ["hello", "world"]


def test_tokenize_case_insensitive():
    indexer = InvertedIndexer()

    words = indexer.tokenize("Good GOOD good")

    assert words == ["good", "good", "good"]


def test_tokenize_empty_text():
    indexer = InvertedIndexer()

    words = indexer.tokenize("")

    assert words == []


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


def test_get_missing_word_entry():
    indexer = InvertedIndexer()

    entry = indexer.get_word_entry("missing")

    assert entry == {}


def test_get_index_returns_dictionary():
    indexer = InvertedIndexer()

    indexer.add_page("page1", "hello world")
    index = indexer.get_index()

    assert isinstance(index, dict)
    assert "hello" in index


def test_get_vocabulary_size():
    indexer = InvertedIndexer()

    indexer.add_page("page1", "hello hello world")

    assert indexer.get_vocabulary_size() == 2


def test_get_statistics():
    indexer = InvertedIndexer()

    indexer.add_page("page1", "hello world")
    indexer.add_page("page2", "hello python")

    stats = indexer.get_statistics()

    assert stats["pages_indexed"] == 2
    assert stats["words_indexed"] == 4
    assert stats["unique_words"] == 3