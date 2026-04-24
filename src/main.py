import json
import os

from src.crawler import WebCrawler
from src.indexer import InvertedIndexer
from src.search import SearchEngine


DATA_FOLDER = "../data"
INDEX_FILE = os.path.join(DATA_FOLDER, "index.json")


def ensure_data_folder():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)


def save_index(index):
    ensure_data_folder()

    with open(INDEX_FILE, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=4)

    print("Index saved successfully.")


def load_index():
    if not os.path.exists(INDEX_FILE):
        print("No saved index found. Run build first.")
        return None

    with open(INDEX_FILE, "r", encoding="utf-8") as file:
        index = json.load(file)

    print("Index loaded successfully.")
    return index


def build_command():
    crawler = WebCrawler()
    pages = crawler.crawl_all_pages()

    indexer = InvertedIndexer()
    index = indexer.build_index(pages)

    save_index(index)


def shell():
    loaded_index = None

    print("COMP3011 Search Engine Tool")
    print("Commands: build, load, print <word>, find <query>, exit")

    while True:
        command = input("\n> ").strip()

        if not command:
            continue

        if command == "exit":
            print("Goodbye.")
            break

        elif command == "build":
            build_command()

        elif command == "load":
            loaded_index = load_index()

        elif command.startswith("print "):
            if loaded_index is None:
                print("Load index first.")
                continue

            word = command[6:].strip()

            if not word:
                print("Enter a word.")
                continue

            engine = SearchEngine(loaded_index)
            engine.print_word(word)

        elif command.startswith("find "):
            if loaded_index is None:
                print("Load index first.")
                continue

            query = command[5:].strip()

            if not query:
                print("Enter a search query.")
                continue

            engine = SearchEngine(loaded_index)
            engine.find(query)

        else:
            print("Unknown command.")


if __name__ == "__main__":
    shell()