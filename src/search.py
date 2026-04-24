import math
import re


class SearchEngine:
    def __init__(self, index):
        """
        index = inverted index dictionary
        """
        self.index = index

    def normalise_query(self, query):
        """
        Converts query into lowercase search terms.
        """
        if not query:
            return []

        return re.findall(r"[a-zA-Z0-9']+", query.lower())

    def print_word(self, word):
        """
        Print postings list for a single word.
        """
        words = self.normalise_query(word)

        if not words:
            print("Enter a valid word.")
            return

        word = words[0]

        if word not in self.index:
            print(f"'{word}' not found in index.")
            return

        print(f"\nWord: {word}")

        for url, stats in self.index[word].items():
            print(f"- {url}")
            print(f"  Frequency: {stats['freq']}")
            print(f"  Positions: {stats['positions']}")

    def find(self, query):
        """
        Find pages containing all query words.
        Results are ranked using a simple TF-IDF style score.
        """
        words = self.normalise_query(query)

        if not words:
            print("Empty query.")
            return []

        page_sets = []

        for word in words:
            if word not in self.index:
                print("No matching pages found.")
                return []

            page_sets.append(set(self.index[word].keys()))

        matching_pages = set.intersection(*page_sets)

        if not matching_pages:
            print("No matching pages found.")
            return []

        ranked_results = []

        total_pages = self.get_total_page_count()

        for page in matching_pages:
            score = 0

            for word in words:
                term_frequency = self.index[word][page]["freq"]
                document_frequency = len(self.index[word])
                inverse_document_frequency = math.log((total_pages + 1) / (document_frequency + 1)) + 1

                score += term_frequency * inverse_document_frequency

            ranked_results.append((page, round(score, 4)))

        ranked_results.sort(key=lambda x: x[1], reverse=True)

        print("\nSearch Results:")

        for page, score in ranked_results:
            print(f"- {page} (score: {score})")

        return ranked_results

    def find_phrase(self, phrase):
        """
        Find pages where all words in the phrase appear next to each other.
        Example:
        find_phrase("good friends")
        """
        words = self.normalise_query(phrase)

        if not words:
            print("Empty phrase.")
            return []

        if len(words) == 1:
            return self.find(words[0])

        for word in words:
            if word not in self.index:
                print("No matching phrase found.")
                return []

        page_sets = [set(self.index[word].keys()) for word in words]
        possible_pages = set.intersection(*page_sets)

        matching_pages = []

        for page in possible_pages:
            first_word_positions = self.index[words[0]][page]["positions"]

            for start_position in first_word_positions:
                phrase_found = True

                for offset, word in enumerate(words[1:], start=1):
                    expected_position = start_position + offset

                    if expected_position not in self.index[word][page]["positions"]:
                        phrase_found = False
                        break

                if phrase_found:
                    score = sum(self.index[word][page]["freq"] for word in words)
                    matching_pages.append((page, score))
                    break

        if not matching_pages:
            print("No matching phrase found.")
            return []

        matching_pages.sort(key=lambda x: x[1], reverse=True)

        print("\nPhrase Search Results:")

        for page, score in matching_pages:
            print(f"- {page} (score: {score})")

        return matching_pages

    def get_total_page_count(self):
        """
        Count unique pages in the whole index.
        """
        pages = set()

        for word_entries in self.index.values():
            pages.update(word_entries.keys())

        return len(pages)