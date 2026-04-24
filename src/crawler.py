import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://quotes.toscrape.com/"
POLITENESS_DELAY = 6


class WebCrawler:
    def __init__(self):
        self.visited_pages = set()

    def fetch_page(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            time.sleep(POLITENESS_DELAY)

            return BeautifulSoup(response.text, "html.parser")

        except Exception as error:
            print(f"Error fetching {url}: {error}")
            return None

    def extract_text(self, soup):
        if soup is None:
            return ""

        page_text = []

        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            text = quote.find("span", class_="text")
            author = quote.find("small", class_="author")
            tags = quote.find_all("a", class_="tag")

            if text:
                page_text.append(text.get_text())

            if author:
                page_text.append(author.get_text())

            for tag in tags:
                page_text.append(tag.get_text())

        return " ".join(page_text)

    def get_next_page(self, soup):
        if soup is None:
            return None

        next_button = soup.find("li", class_="next")

        if next_button:
            link = next_button.find("a")
            if link:
                return urljoin(BASE_URL, link["href"])

        return None

    def crawl_all_pages(self):
        current_url = BASE_URL
        crawled_data = {}

        while current_url and current_url not in self.visited_pages:
            print(f"Crawling: {current_url}")

            soup = self.fetch_page(current_url)

            if soup is None:
                break

            text = self.extract_text(soup)

            crawled_data[current_url] = text
            self.visited_pages.add(current_url)

            current_url = self.get_next_page(soup)

        return crawled_data