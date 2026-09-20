from unittest.mock import Mock

from src.scraper.http_client import HTTPClient
from src.scraper.parser import BookParser
from src.scraper.cleaner import BookDataCleaner
from src.scraper.main import (
    ScraperPipeline,
    filter_books,
    remove_duplicates,
)


# ==========================================
# MOCK HTML
# ==========================================

MOCK_HTML = """
<html>
    <body>

        <article class="product_pod">

            <h3>
                <a href="book-one.html"
                   title="Book One">
                    Book One
                </a>
            </h3>

            <p class="price_color">
                £10.99
            </p>

            <p class="star-rating Three">
            </p>

            <p class="availability">
                In stock
            </p>

        </article>

        <article class="product_pod">

            <h3>
                <a href="book-two.html"
                   title="Book Two">
                    Book Two
                </a>
            </h3>

            <p class="price_color">
                £25.50
            </p>

            <p class="star-rating Five">
            </p>

            <p class="availability">
                In stock
            </p>

        </article>

        <li class="next">
            <a href="page-2.html">
                next
            </a>
        </li>

    </body>
</html>
"""


# ==========================================
# EXISTING TEST
# ==========================================

def test_scraping_pipeline():
    client = HTTPClient()

    try:
        html = client.fetch(
            "https://books.toscrape.com/"
        )

        parser = BookParser()
        cleaner = BookDataCleaner()

        books = parser.parse(
            html,
            "https://books.toscrape.com/"
        )

        cleaned_books = cleaner.clean_many(
            books
        )

        assert len(books) == 20
        assert len(cleaned_books) == 20

        for book in cleaned_books:
            assert book["title"]
            assert book["price"] is not None
            assert book["rating"] is not None
            assert book["availability"]
            assert book["url"].startswith("http")

    finally:
        client.close()


# ==========================================
# EXISTING DATA QUALITY TEST
# ==========================================

def test_pipeline_data_quality():
    client = HTTPClient()

    try:
        html = client.fetch(
            "https://books.toscrape.com/"
        )

        parser = BookParser()
        cleaner = BookDataCleaner()

        books = parser.parse(
            html,
            "https://books.toscrape.com/"
        )

        cleaned_books = cleaner.clean_many(
            books
        )

        for book in cleaned_books:
            assert isinstance(
                book["title"],
                str
            )

            assert isinstance(
                book["price"],
                float
            )

            assert isinstance(
                book["rating"],
                int
            )

            assert isinstance(
                book["availability"],
                str
            )

            assert isinstance(
                book["url"],
                str
            )

    finally:
        client.close()


# ==========================================
# TASK 16
# MOCK SCRAPING PIPELINE
# ==========================================

def test_mock_scraping_pipeline():
    """Test the pipeline without accessing the internet."""

    pipeline = ScraperPipeline()

    try:
        pipeline.client.fetch = Mock(
            return_value=MOCK_HTML
        )

        html = pipeline.fetch_page(
            "https://example.com/"
        )

        books = pipeline.parse_page(
            html,
            "https://example.com/"
        )

        assert len(books) == 2

        assert books[0]["title"] == "Book One"
        assert books[0]["price"] == 10.99
        assert books[0]["rating"] == 3
        assert books[0]["availability"] == "In stock"

        assert books[1]["title"] == "Book Two"
        assert books[1]["price"] == 25.50
        assert books[1]["rating"] == 5
        assert books[1]["availability"] == "In stock"

    finally:
        pipeline.close()


# ==========================================
# TEST NEXT PAGE
# ==========================================

def test_get_next_url():
    """Test next-page URL detection."""

    next_url = ScraperPipeline.get_next_url(
        MOCK_HTML,
        "https://example.com/index.html"
    )

    assert next_url == (
        "https://example.com/page-2.html"
    )


# ==========================================
# TEST NO NEXT PAGE
# ==========================================

def test_get_next_url_when_missing():
    """Test when there is no next page."""

    html = """
    <html>
        <body>

            <article class="product_pod">
            </article>

        </body>
    </html>
    """

    next_url = ScraperPipeline.get_next_url(
        html,
        "https://example.com/index.html"
    )

    assert next_url is None


# ==========================================
# TEST FILTERING
# ==========================================

def test_filter_books():
    """Test price and rating filtering."""

    books = [
        {
            "title": "Cheap Book",
            "price": 5.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://example.com/1",
        },
        {
            "title": "Expensive Book",
            "price": 50.00,
            "rating": 5,
            "availability": "In stock",
            "url": "https://example.com/2",
        },
    ]

    result = filter_books(
        books,
        min_price=10,
        rating=5
    )

    assert len(result) == 1

    assert result[0]["title"] == (
        "Expensive Book"
    )


# ==========================================
# TEST DUPLICATE REMOVAL
# ==========================================

def test_remove_duplicates():
    """Test duplicate book removal."""

    books = [
        {
            "title": "Book One",
            "price": 10.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://example.com/book",
        },
        {
            "title": "Book One",
            "price": 10.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://example.com/book",
        },
        {
            "title": "Book Two",
            "price": 20.00,
            "rating": 5,
            "availability": "In stock",
            "url": "https://example.com/book2",
        },
    ]

    result = remove_duplicates(
        books
    )

    assert len(result) == 2

    assert result[0]["title"] == "Book One"
    assert result[1]["title"] == "Book Two"