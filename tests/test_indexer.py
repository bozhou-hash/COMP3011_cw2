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
        }
    }


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


def test_case_insensitive_search():
    engine = SearchEngine(sample_index())

    results = engine.find("GOOD")

    assert len(results) == 2