import json
import os

from src.crawler import WebCrawler
from src.indexer import InvertedIndexer
from src.search import SearchEngine
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"
INDEX_FILE = DATA_FOLDER / "index.json"


def ensure_data_folder():
    DATA_FOLDER.mkdir(exist_ok=True)


def save_index(index):
    ensure_data_folder()

    with open(INDEX_FILE, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=4)

    print(f"Index saved successfully to {INDEX_FILE}")

def load_index():
    if not INDEX_FILE.exists():
        print("No saved index found. Run build first.")
        return None

    with open(INDEX_FILE, "r", encoding="utf-8") as file:
        index = json.load(file)

    print(f"Index loaded successfully from {INDEX_FILE}")
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