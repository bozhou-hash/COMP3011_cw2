from src.search import SearchEngine


def sample_index():
    return {
        "good": {
            "page1": {"freq": 2, "positions": [0, 4]},
            "page2": {"freq": 1, "positions": [2]}
        },
        "friends": {
            "page1": {"freq": 1, "positions": [5]},
            "page3": {"freq": 3, "positions": [1, 2, 3]}
        },
        "life": {
            "page2": {"freq": 1, "positions": [0]}
        },
        "hello": {
            "page4": {"freq": 1, "positions": [0]}
        },
        "world": {
            "page4": {"freq": 1, "positions": [1]},
            "page5": {"freq": 1, "positions": [3]}
        }
    }


def test_normalise_query_lowercase():
    engine = SearchEngine(sample_index())

    result = engine.normalise_query("GOOD Friends!")

    assert result == ["good", "friends"]


def test_normalise_query_empty():
    engine = SearchEngine(sample_index())

    result = engine.normalise_query("")

    assert result == []


def test_find_single_word():
    engine = SearchEngine(sample_index())

    results = engine.find("life")

    assert len(results) == 1
    assert results[0][0] == "page2"


def test_find_multiple_words():
    engine = SearchEngine(sample_index())

    results = engine.find("good friends")

    assert len(results) == 1
    assert results[0][0] == "page1"


def test_find_missing_word():
    engine = SearchEngine(sample_index())

    results = engine.find("unknown")

    assert results == []


def test_find_partial_missing():
    engine = SearchEngine(sample_index())

    results = engine.find("good unknown")

    assert results == []


def test_find_empty_query():
    engine = SearchEngine(sample_index())

    results = engine.find("")

    assert results == []


def test_case_insensitive_search():
    engine = SearchEngine(sample_index())

    results = engine.find("GOOD")

    assert len(results) == 2


def test_find_results_are_ranked():
    engine = SearchEngine(sample_index())

    results = engine.find("good")

    assert results[0][1] >= results[1][1]


def test_find_phrase_success():
    engine = SearchEngine(sample_index())

    results = engine.find_phrase("good friends")

    assert len(results) == 1
    assert results[0][0] == "page1"


def test_find_phrase_not_adjacent():
    engine = SearchEngine(sample_index())

    results = engine.find_phrase("friends good")

    assert results == []


def test_find_phrase_single_word():
    engine = SearchEngine(sample_index())

    results = engine.find_phrase("life")

    assert len(results) == 1
    assert results[0][0] == "page2"


def test_find_phrase_missing_word():
    engine = SearchEngine(sample_index())

    results = engine.find_phrase("good unknown")

    assert results == []


def test_get_total_page_count():
    engine = SearchEngine(sample_index())

    total_pages = engine.get_total_page_count()

    assert total_pages == 5