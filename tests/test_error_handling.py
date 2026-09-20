import pytest
import requests

from src.scraper.http_client import HTTPClient
from src.scraper.parser import BookParser
from src.scraper.cleaner import BookDataCleaner


# ==========================================
# TEST INVALID URL
# ==========================================

def test_invalid_url():
    client = HTTPClient()

    try:
        with pytest.raises(
            (
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
            )
        ):
            client.fetch(
                "https://books.toscrape.com/this-page-does-not-exist.html"
            )

    finally:
        client.close()


# ==========================================
# TEST HTTP CONNECTION ERROR
# ==========================================

def test_http_connection_error():
    """Test that connection errors are raised."""

    client = HTTPClient()

    try:
        client.session.get = lambda *args, **kwargs: (
            (_ for _ in ()).throw(
                requests.exceptions.ConnectionError(
                    "Connection failed"
                )
            )
        )

        with pytest.raises(
            requests.exceptions.ConnectionError
        ):
            client.fetch(
                "https://example.com/"
            )

    finally:
        client.close()


# ==========================================
# TEST PARSER INVALID HTML
# ==========================================

def test_parser_invalid_html():
    """Test parser with HTML containing no books."""

    parser = BookParser()

    html = """
    <html>
        <body>
            <h1>This is not a book page</h1>
        </body>
    </html>
    """

    books = parser.parse(
        html,
        "https://example.com/"
    )

    assert books == []


# ==========================================
# TEST PARSER EMPTY HTML
# ==========================================

def test_parser_empty_html():
    """Test parser with empty HTML."""

    parser = BookParser()

    books = parser.parse(
        "",
        "https://example.com/"
    )

    assert books == []


# ==========================================
# TEST CLEANER MISSING REQUIRED FIELD
# ==========================================

def test_cleaner_missing_required_field():
    """Test cleaner when a required field is missing."""

    cleaner = BookDataCleaner()

    book = {
        "title": "Test Book",
        "price": 10.99,
        "rating": 5,
        "availability": "In stock",
    }

    result = cleaner.clean(
        book
    )

    assert result is None


# ==========================================
# TEST CLEANER INVALID PRICE
# ==========================================

def test_cleaner_invalid_price():
    """Test cleaner with a negative price."""

    cleaner = BookDataCleaner()

    book = {
        "title": "Test Book",
        "price": -10,
        "rating": 5,
        "availability": "In stock",
        "url": "https://example.com/book",
    }

    result = cleaner.clean(
        book
    )

    assert result is None


# ==========================================
# TEST CLEANER INVALID RATING
# ==========================================

def test_cleaner_invalid_rating():
    """Test cleaner with an invalid rating."""

    cleaner = BookDataCleaner()

    book = {
        "title": "Test Book",
        "price": 10.99,
        "rating": 10,
        "availability": "In stock",
        "url": "https://example.com/book",
    }

    result = cleaner.clean(
        book
    )

    assert result is None


# ==========================================
# TEST CLEANER EMPTY TITLE
# ==========================================

def test_cleaner_empty_title():
    """Test cleaner with an empty title."""

    cleaner = BookDataCleaner()

    book = {
        "title": "",
        "price": 10.99,
        "rating": 5,
        "availability": "In stock",
        "url": "https://example.com/book",
    }

    result = cleaner.clean(
        book
    )

    assert result is None


# ==========================================
# TEST CLEANER INVALID URL
# ==========================================

def test_cleaner_invalid_url():
    """Test cleaner with an invalid URL."""

    cleaner = BookDataCleaner()

    book = {
        "title": "Test Book",
        "price": 10.99,
        "rating": 5,
        "availability": "In stock",
        "url": "not-a-valid-url",
    }

    result = cleaner.clean(
        book
    )

    assert result is None


# ==========================================
# TEST CLEAN MANY WITH INVALID BOOKS
# ==========================================

def test_clean_many_with_invalid_books():
    """Test cleaning valid and invalid books together."""

    cleaner = BookDataCleaner()

    books = [
        {
            "title": "Valid Book",
            "price": 10.99,
            "rating": 5,
            "availability": "In stock",
            "url": "https://example.com/valid",
        },
        {
            "title": "",
            "price": 20.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://example.com/invalid",
        },
        {
            "title": "Another Valid Book",
            "price": 15.50,
            "rating": 4,
            "availability": "In stock",
            "url": "https://example.com/valid2",
        },
    ]

    result = cleaner.clean_many(
        books
    )

    assert len(result) == 2

    assert result[0]["title"] == (
        "Valid Book"
    )

    assert result[1]["title"] == (
        "Another Valid Book"
    )