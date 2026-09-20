from src.scraper.cleaner import BookDataCleaner


cleaner = BookDataCleaner()


def test_valid_book():
    book = {
        "title": "Test Book",
        "price": 25.50,
        "rating": 5,
        "availability": "In stock",
        "url": "https://example.com/book",
    }

    result = cleaner.clean(book)

    assert result is not None
    assert result["title"] == "Test Book"
    assert result["price"] == 25.50
    assert result["rating"] == 5


def test_empty_title():
    book = {
        "title": "",
        "price": 25.50,
        "rating": 5,
        "availability": "In stock",
        "url": "https://example.com/book",
    }

    result = cleaner.clean(book)

    assert result is None


def test_negative_price():
    book = {
        "title": "Test Book",
        "price": -10,
        "rating": 5,
        "availability": "In stock",
        "url": "https://example.com/book",
    }

    result = cleaner.clean(book)

    assert result is None


def test_invalid_rating():
    book = {
        "title": "Test Book",
        "price": 25.50,
        "rating": 6,
        "availability": "In stock",
        "url": "https://example.com/book",
    }

    result = cleaner.clean(book)

    assert result is None


def test_invalid_url():
    book = {
        "title": "Test Book",
        "price": 25.50,
        "rating": 5,
        "availability": "In stock",
        "url": "not-a-url",
    }

    result = cleaner.clean(book)

    assert result is None


def test_missing_required_field():
    book = {
        "title": "Test Book",
        "price": 25.50,
        "rating": 5,
        "availability": "In stock",
    }

    result = cleaner.clean(book)

    assert result is None