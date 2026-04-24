import re
from collections import defaultdict


class InvertedIndexer:
    def __init__(self):
        """
        Structure:
        {
            word: {
                page_url: {
                    "freq": int,
                    "positions": [int, int]
                }
            }
        }
        """
        self.index = defaultdict(dict)

    def tokenize(self, text):
        """
        Convert text into lowercase words.
        Keeps only letters/numbers/apostrophes.
        """
        if not text:
            return []

        return re.findall(r"[a-zA-Z0-9']+", text.lower())

    def add_page(self, url, text):
        """
        Add one crawled page into inverted index.
        """
        words = self.tokenize(text)

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
        crawled_data format:
        {
            url: text
        }
        """
        for url, text in crawled_data.items():
            self.add_page(url, text)

        return self.index

    def get_word_entry(self, word):
        """
        Return postings list for a word.
        """
        return self.index.get(word.lower(), {})

    def get_index(self):
        """
        Return whole index.
        """
        return self.index