import math
import re


class SearchEngine:
    def __init__(self, index):
        """
        Search engine for querying an inverted index.
        """
        self.index = index

    def normalise_query(self, query):
        """
        Convert a user query into lowercase searchable terms.
        """
        if not query:
            return []

        return re.findall(r"[a-zA-Z0-9']+", query.lower())

    def print_word(self, word):
        """
        Print the inverted index entry for a single word.
        """
        words = self.normalise_query(word)

        if not words:
            print("Enter a valid word.")
            return {}

        word = words[0]
        entry = self.index.get(word, {})

        if not entry:
            print(f"'{word}' not found in index.")
            return {}

        print(f"\nWord: {word}")

        for url, stats in entry.items():
            print(f"- {url}")
            print(f"  Frequency: {stats['freq']}")
            print(f"  Positions: {stats['positions']}")

        return entry

    def find(self, query):
        """
        Find pages containing all query words.

        Results are ranked using a simple TF-IDF style score:
        - term frequency rewards repeated terms on a page
        - inverse document frequency rewards more distinctive terms
        """
        words = self.normalise_query(query)

        if not words:
            print("Empty query.")
            return []

        matching_pages = self.get_pages_containing_all_words(words)

        if not matching_pages:
            print("No matching pages found.")
            return []

        ranked_results = self.rank_pages(words, matching_pages)

        print("\nSearch Results:")

        for page, score in ranked_results:
            print(f"- {page} (score: {score})")

        return ranked_results

    def find_phrase(self, phrase):
        """
        Find pages where all words in a phrase appear next to each other.
        """
        words = self.normalise_query(phrase)

        if not words:
            print("Empty phrase.")
            return []

        if len(words) == 1:
            return self.find(words[0])

        possible_pages = self.get_pages_containing_all_words(words)

        if not possible_pages:
            print("No matching phrase found.")
            return []

        matching_pages = []

        for page in possible_pages:
            if self.page_contains_phrase(page, words):
                score = self.calculate_phrase_score(page, words)
                matching_pages.append((page, score))

        if not matching_pages:
            print("No matching phrase found.")
            return []

        matching_pages.sort(key=lambda result: result[1], reverse=True)

        print("\nPhrase Search Results:")

        for page, score in matching_pages:
            print(f"- {page} (score: {score})")

        return matching_pages

    def get_pages_containing_all_words(self, words):
        """
        Return pages that contain every word in the query.
        """
        page_sets = []

        for word in words:
            if word not in self.index:
                return set()

            page_sets.append(set(self.index[word].keys()))

        return set.intersection(*page_sets) if page_sets else set()

    def rank_pages(self, words, pages):
        """
        Rank matching pages using a simple TF-IDF style score.
        """
        ranked_results = []
        total_pages = self.get_total_page_count()

        for page in pages:
            score = 0

            for word in words:
                score += self.calculate_tfidf_score(word, page, total_pages)

            ranked_results.append((page, round(score, 4)))

        ranked_results.sort(key=lambda result: result[1], reverse=True)
        return ranked_results

    def calculate_tfidf_score(self, word, page, total_pages):
        """
        Calculate a simple TF-IDF style score for one word on one page.
        """
        term_frequency = self.index[word][page]["freq"]
        document_frequency = len(self.index[word])
        inverse_document_frequency = math.log((total_pages + 1) / (document_frequency + 1)) + 1

        return term_frequency * inverse_document_frequency

    def page_contains_phrase(self, page, words):
        """
        Check whether words appear consecutively on a page using stored positions.
        """
        first_word_positions = self.index[words[0]][page]["positions"]

        for start_position in first_word_positions:
            phrase_found = True

            for offset, word in enumerate(words[1:], start=1):
                expected_position = start_position + offset
                word_positions = self.index[word][page]["positions"]

                if expected_position not in word_positions:
                    phrase_found = False
                    break

            if phrase_found:
                return True

        return False

    def calculate_phrase_score(self, page, words):
        """
        Score phrase results using total frequency of phrase terms on the page.
        """
        return sum(self.index[word][page]["freq"] for word in words)

    def get_total_page_count(self):
        """
        Count unique pages in the whole index.
        """
        pages = set()

        for word_entries in self.index.values():
            pages.update(word_entries.keys())

        return len(pages)