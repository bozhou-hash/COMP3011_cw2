class SearchEngine:
    def __init__(self, index):
        self.index = index

    def print_word(self, word):
        word = word.lower()

        if word not in self.index:
            print(f"'{word}' not found in index.")
            return

        print(f"\nWord: {word}")

        for url, stats in self.index[word].items():
            print(f"- {url}")
            print(f"  Frequency: {stats['freq']}")
            print(f"  Positions: {stats['positions']}")

    def find(self, query):
        words = query.lower().split()

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

        for page in matching_pages:
            score = sum(self.index[word][page]["freq"] for word in words)
            ranked_results.append((page, score))

        ranked_results.sort(key=lambda x: x[1], reverse=True)

        print("\nSearch Results:")

        for page, score in ranked_results:
            print(f"- {page} (score: {score})")

        return ranked_results