from src.scraper.cleaner import BookDataCleaner


cleaner = BookDataCleaner()


books = [
    {
        "title": "Book A",
        "price": 10.00,
        "rating": 5,
        "availability": "In stock",
        "url": "https://example.com/book-a",
    },
    {
        "title": "Book B",
        "price": 20.00,
        "rating": 3,
        "availability": "In stock",
        "url": "https://example.com/book-b",
    },
    {
        "title": "",
        "price": 30.00,
        "rating": 4,
        "availability": "In stock",
        "url": "https://example.com/book-c",
    },
]


def test_clean_many_returns_valid_books():
    cleaned_books = cleaner.clean_many(books)

    assert len(cleaned_books) == 2


def test_clean_many_removes_invalid_books():
    cleaned_books = cleaner.clean_many(books)

    titles = [
        book["title"]
        for book in cleaned_books
    ]

    assert "Book A" in titles
    assert "Book B" in titles
    assert "" not in titles


def test_clean_many_preserves_data():
    cleaned_books = cleaner.clean_many(books)

    assert cleaned_books[0]["title"] == "Book A"
    assert cleaned_books[0]["price"] == 10.00
    assert cleaned_books[0]["rating"] == 5


def test_clean_many_empty_list():
    cleaned_books = cleaner.clean_many([])

    assert cleaned_books == []