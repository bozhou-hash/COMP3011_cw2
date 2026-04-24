# COMP3011 Coursework 2 – Search Engine Tool

## Overview

This project is a Python-based command-line search engine developed for **COMP3011: Web Services and Web Data**.

The tool crawls the website:

https://quotes.toscrape.com/

It then builds an **inverted index** of the words found on each page and allows users to search for words or phrases using a command-line interface.

The project demonstrates key search engine concepts including:

- Web crawling
- Index construction
- Persistent storage
- Query processing
- Ranked retrieval
- Phrase searching
- Software testing
- Version control workflow

---

## Table of Contents

1. [Features](#features)  
2. [Project Structure](#project-structure)  
3. [Installation](#installation) 
4. [Commands](#available-commands)  
5. [Example Usage](#example-usage)  
6. [Testing](#testing)  
7. [Design Decisions](#design-decisions)  
8. [Generative AI Usage Declaration](#generative-ai-usage-declaration)  
9. [Future Improvements](#future-improvements)

---

## Features

### Core Features

- Crawls all pages of the target website
- Respects a **6-second politeness delay** between requests
- Extracts searchable content:
  - Quote text
  - Author names
  - Tags
- Builds an inverted index containing:
  - Word frequency
  - Word positions
- Saves compiled index to file
- Loads saved index from file
- Case-insensitive searching

### Search Features

- Single-word search
- Multi-word AND search
- Phrase search using positional indexing

Example:

```text
find life
find good friends
find "good friends"
```

### Ranking Features

Search results are ranked using a simple **TF-IDF style relevance score**.



### Quality Features

- Modular code structure
- Pytest automated testing
- 38 passing tests
- Strong code coverage on core modules

---

## Project Structure

```text
COMP3011_cw2/
│
├── src/
│   ├── crawler.py
│   ├── indexer.py
│   ├── search.py
│   └── main.py
│
├── tests/
│   ├── test_crawler.py
│   ├── test_indexer.py
│   └── test_search.py
│
├── data/
│   └── index.json
│
├── requirements.txt
└── README.md
```

---

## Installation

1. Clone Repository
```text
git clone https://github.com/bozhou-hash/COMP3011_cw2.git
cd COMP3011_cw2
```
2. Create Virtual Environment
```text
python -m venv .venv
```
3. Activate Environment

#### Windows Powershell
```text
.venv\Scripts\activate
```

#### Mac/Linux
```text
source .venv/bin/activate
```
4. Install Dependencies
```text
pip install -r requirements.txt
```

#### Dependencies
```text
requests
beautifulsoup4
pytest
pytest-cov
```

5. Running the Program

#### From the project root:
```text
python -m src.main
```

---

## Available Commands
```text
build
load
print <word>
find <query>
find "phrase query"
help
exit
```

---

## Example Usage

### Build Index
```text
> build
```
Crawls all pages and creates:
```text
data/index.json
```

### Load Existing Index
```text
> load
```

### Print Inverted Index Entry
```text
> print life
```

### Search for a Word
```text
> find truth
```

### Search Multiple Words
```text
> find good friends
```
Returns pages containing all words.

### Phrase Search
```text
> find "good friends"
```
Returns pages where words appear consecutively.

--- 

## Testing

Run all tests:
```text
pytest -v
```

Run coverage:
```text
pytest --cov=src.crawler --cov=src.indexer --cov=src.search
```

Current results:
```text
38 tests passed
92%+ core module coverage
```

---

## Design Decisions

### Inverted Index
Words are stored in the format:
```python
{
  word: {
    page_url: {
      "freq": count,
      "positions": [...]
    }
  }
}
```

This allows:
- Fast lookup
- Frequency ranking
- Phrase searching and positions

A simple TF-IDF style score was used because: 
- Frequent terms in a page increase relevance
- Rare terms across pages are more valuable

---

## Error Handling

The system handles:
- Missing index files
- Empty queries
- Unknown commands
- Missing words
- Failed network requests

--- 

## Generative AI Usage Declaration

Generative AI tools were used during development for:
- Code review suggestions
- Debugging support
- Testing ideas
- Documentation drafting
- Refactoring recommendations

All generated suggestions were manually reviewed, tested, modified where necessary, and fully understood before inclusion.

AI outputs were not accepted blindly.

---

## Future Improvements

Possible extensions include:

- Stop-word removal
- Stemming / lemmatisation
- Boolean queries (AND / OR / NOT)
- Faster compress index storage
- Page caching
- More advanced ranking models