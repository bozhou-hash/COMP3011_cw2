import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com/"
POLITENESS_DELAY = 6
REQUEST_TIMEOUT = 10


class WebCrawler:
    def __init__(self, base_url=BASE_URL, politeness_delay=POLITENESS_DELAY):
        self.base_url = base_url
        self.politeness_delay = politeness_delay
        self.visited_pages = set()

    def fetch_page(self, url):
        """
        Download a webpage and return a BeautifulSoup object.

        A politeness delay is applied after each successful request to avoid
        sending requests to the target website too quickly.
        """
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            time.sleep(self.politeness_delay)

            return BeautifulSoup(response.text, "html.parser")

        except requests.RequestException as error:
            print(f"Error fetching {url}: {error}")
            return None

    def extract_text(self, soup):
        """
        Extract searchable text from one quotes.toscrape.com page.

        The index uses quote text, author names, and tags because these are the
        main meaningful content areas of the target website.
        """
        if soup is None:
            return ""

        page_text = []

        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            quote_text = quote.find("span", class_="text")
            author = quote.find("small", class_="author")
            tags = quote.find_all("a", class_="tag")

            if quote_text:
                page_text.append(quote_text.get_text(strip=True))

            if author:
                page_text.append(author.get_text(strip=True))

            for tag in tags:
                page_text.append(tag.get_text(strip=True))

        return " ".join(page_text)

    def get_next_page(self, soup):
        """
        Return the absolute URL of the next page, or None if there is no next page.
        """
        if soup is None:
            return None

        next_button = soup.find("li", class_="next")

        if next_button is None:
            return None

        link = next_button.find("a")

        if link is None or not link.get("href"):
            return None

        return urljoin(self.base_url, link["href"])

    def crawl_all_pages(self):
        """
        Crawl all quote pages starting from the base URL.

        Returns:
            dict: {page_url: extracted_page_text}
        """
        current_url = self.base_url
        crawled_data = {}

        while current_url and current_url not in self.visited_pages:
            print(f"Crawling: {current_url}")

            soup = self.fetch_page(current_url)

            if soup is None:
                print("Stopping crawl because the page could not be fetched.")
                break

            crawled_data[current_url] = self.extract_text(soup)
            self.visited_pages.add(current_url)

            current_url = self.get_next_page(soup)

        print(f"Crawling complete. Pages crawled: {len(crawled_data)}")
        return crawled_data