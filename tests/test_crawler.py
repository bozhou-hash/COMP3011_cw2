from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from src.crawler import WebCrawler


def test_extract_text():
    crawler = WebCrawler()

    html = """
    <div class="quote">
        <span class="text">Hello world</span>
        <small class="author">Calvin</small>
        <a class="tag">life</a>
        <a class="tag">truth</a>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")
    text = crawler.extract_text(soup)

    assert "Hello world" in text
    assert "Calvin" in text
    assert "life" in text
    assert "truth" in text


@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_fetch_page_success(mock_get, mock_sleep):
    mock_response = Mock()
    mock_response.text = "<html></html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    crawler = WebCrawler()
    soup = crawler.fetch_page("https://example.com")

    assert soup is not None
    mock_sleep.assert_called_once()


@patch("src.crawler.requests.get")
def test_fetch_page_failure(mock_get):
    mock_get.side_effect = Exception("Network error")

    crawler = WebCrawler()
    soup = crawler.fetch_page("https://example.com")

    assert soup is None


def test_get_next_page():
    crawler = WebCrawler()

    html = """
    <li class="next">
        <a href="/page/2/">Next</a>
    </li>
    """

    soup = BeautifulSoup(html, "html.parser")
    next_page = crawler.get_next_page(soup)

    assert next_page == "https://quotes.toscrape.com/page/2/"


def test_get_next_page_missing():
    crawler = WebCrawler()

    soup = BeautifulSoup("<html></html>", "html.parser")
    next_page = crawler.get_next_page(soup)

    assert next_page is None