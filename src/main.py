import json
from pathlib import Path

from src.crawler import WebCrawler
from src.indexer import InvertedIndexer
from src.search import SearchEngine


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"
INDEX_FILE = DATA_FOLDER / "index.json"


def ensure_data_folder():
    """
    Create the data folder if it does not already exist.
    """
    DATA_FOLDER.mkdir(exist_ok=True)


def save_index(index):
    """
    Save the inverted index to a JSON file.
    """
    ensure_data_folder()

    with open(INDEX_FILE, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=4)

    print(f"Index saved successfully to {INDEX_FILE}")


def load_index():
    """
    Load the inverted index from the JSON file.
    """
    if not INDEX_FILE.exists():
        print("No saved index found. Run build first.")
        return None

    with open(INDEX_FILE, "r", encoding="utf-8") as file:
        index = json.load(file)

    print(f"Index loaded successfully from {INDEX_FILE}")
    return index


def build_command():
    """
    Crawl the website, build the inverted index, and save it to disk.
    """
    crawler = WebCrawler()
    pages = crawler.crawl_all_pages()

    if not pages:
        print("No pages were crawled. Index was not created.")
        return None

    indexer = InvertedIndexer()
    index = indexer.build_index(pages)

    save_index(index)

    stats = indexer.get_statistics()
    print("Index statistics:")
    print(f"- Pages indexed: {stats['pages_indexed']}")
    print(f"- Words indexed: {stats['words_indexed']}")
    print(f"- Unique words: {stats['unique_words']}")

    return index


def create_search_engine(loaded_index):
    """
    Create a SearchEngine only when an index has been loaded.
    """
    if loaded_index is None:
        print("Load index first.")
        return None

    return SearchEngine(loaded_index)


def handle_print_command(command, loaded_index):
    """
    Handle the print <word> command.
    """
    engine = create_search_engine(loaded_index)

    if engine is None:
        return

    word = command.removeprefix("print").strip()

    if not word:
        print("Enter a word.")
        return

    engine.print_word(word)


def handle_find_command(command, loaded_index):
    """
    Handle the find <query> command.

    Quoted queries are treated as phrase searches.
    Example:
        find "good friends"
    """
    engine = create_search_engine(loaded_index)

    if engine is None:
        return

    query = command.removeprefix("find").strip()

    if not query:
        print("Enter a search query.")
        return

    if query.startswith('"') and query.endswith('"') and len(query) > 1:
        phrase = query[1:-1].strip()

        if not phrase:
            print("Enter a valid phrase.")
            return

        engine.find_phrase(phrase)
    else:
        engine.find(query)


def print_help():
    """
    Print available CLI commands.
    """
    print("\nAvailable commands:")
    print("  build                 Crawl website, build index, and save it")
    print("  load                  Load saved index from data/index.json")
    print("  print <word>          Print inverted index entry for a word")
    print("  find <query>          Find pages containing all query terms")
    print('  find "phrase query"   Find pages containing an exact phrase')
    print("  help                  Show this help message")
    print("  exit                  Exit the program")


def shell():
    """
    Run the command-line interface.
    """
    loaded_index = None

    print("COMP3011 Search Engine Tool")
    print_help()

    while True:
        command = input("\n> ").strip()

        if not command:
            continue

        if command == "exit":
            print("Goodbye.")
            break

        if command == "help":
            print_help()

        elif command == "build":
            loaded_index = build_command()

        elif command == "load":
            loaded_index = load_index()

        elif command.startswith("print"):
            handle_print_command(command, loaded_index)

        elif command.startswith("find"):
            handle_find_command(command, loaded_index)

        else:
            print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    shell()