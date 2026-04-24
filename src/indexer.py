import re
from collections import defaultdict


class InvertedIndexer:
    def __init__(self):
        """
        Inverted index structure:

        {
            word: {
                page_url: {
                    "freq": int,
                    "positions": [int, int, ...]
                }
            }
        }
        """
        self.index = defaultdict(dict)
        self.total_pages = 0
        self.total_words = 0

    def tokenize(self, text):
        """
        Convert text into lowercase searchable tokens.

        Keeps:
        - letters
        - numbers
        - apostrophes

        Example:
        "Don't Stop Believing!" -> ["don't", "stop", "believing"]
        """
        if not text:
            return []

        return re.findall(r"[a-zA-Z0-9']+", text.lower())

    def add_page(self, url, text):
        """
        Add one crawled page to the inverted index.
        """
        words = self.tokenize(text)

        if not words:
            return

        self.total_pages += 1
        self.total_words += len(words)

        for position, word in enumerate(words):
            if url not in self.index[word]:
                self.index[word][url] = {
                    "freq": 0,
                    "positions": []
                }

            self.index[word][url]["freq"] += 1
            self.index[word][url]["positions"].append(position)

    def build_index(self, crawled_data):
        """
        Build an inverted index from crawled data.

        crawled_data format:
        {
            url: page_text
        }
        """
        self.index.clear()
        self.total_pages = 0
        self.total_words = 0

        for url, text in crawled_data.items():
            self.add_page(url, text)

        return self.index

    def get_word_entry(self, word):
        """
        Return postings list for one word.
        """
        if not word:
            return {}

        return self.index.get(word.lower(), {})

    def get_index(self):
        """
        Return full inverted index.
        """
        return dict(self.index)

    def get_vocabulary_size(self):
        """
        Return number of unique indexed words.
        """
        return len(self.index)

    def get_statistics(self):
        """
        Return useful index statistics.
        """
        return {
            "pages_indexed": self.total_pages,
            "words_indexed": self.total_words,
            "unique_words": self.get_vocabulary_size()
        }