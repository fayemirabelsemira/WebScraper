from src.scraper.analyzer import BookAnalyzer


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
        "title": "Book C",
        "price": 30.00,
        "rating": 4,
        "availability": "In stock",
        "url": "https://example.com/book-c",
    },
    {
        "title": "Book D",
        "price": 40.00,
        "rating": 5,
        "availability": "Out of stock",
        "url": "https://example.com/book-d",
    },
]


def test_total_books():
    analyzer = BookAnalyzer(books)

    assert analyzer.total_books() == 4


def test_average_price():
    analyzer = BookAnalyzer(books)

    assert analyzer.average_price() == 25.00


def test_average_rating():
    analyzer = BookAnalyzer(books)

    assert analyzer.average_rating() == 4.25


def test_most_expensive():
    analyzer = BookAnalyzer(books)

    assert analyzer.most_expensive()["title"] == "Book D"


def test_cheapest():
    analyzer = BookAnalyzer(books)

    assert analyzer.cheapest()["title"] == "Book A"


def test_rating_counts():
    analyzer = BookAnalyzer(books)

    expected_counts = {
        1: 0,
        2: 0,
        3: 1,
        4: 1,
        5: 2,
    }

    assert analyzer.rating_counts() == expected_counts


def test_most_common_rating():
    analyzer = BookAnalyzer(books)

    assert analyzer.most_common_rating() == 5


def test_availability_counts():
    analyzer = BookAnalyzer(books)

    expected = {
        "In stock": 3,
        "Out of stock": 1,
    }

    assert analyzer.availability_counts() == expected


def test_average_price_by_rating():
    analyzer = BookAnalyzer(books)

    expected = {
        1: 0.0,
        2: 0.0,
        3: 20.00,
        4: 30.00,
        5: 25.00,
    }

    assert analyzer.average_price_by_rating() == expected


def test_highest_rated_books():
    analyzer = BookAnalyzer(books)

    result = analyzer.highest_rated_books()

    assert len(result) == 2
    assert result[0]["title"] == "Book A"
    assert result[1]["title"] == "Book D"


def test_lowest_rated_books():
    analyzer = BookAnalyzer(books)

    result = analyzer.lowest_rated_books()

    assert len(result) == 1
    assert result[0]["title"] == "Book B"

def test_minimum_price():
    books = [
        {
            "title": "Book A",
            "price": 20.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://example.com/a",
        },
        {
            "title": "Book B",
            "price": 10.00,
            "rating": 4,
            "availability": "In stock",
            "url": "https://example.com/b",
        },
        {
            "title": "Book C",
            "price": 30.00,
            "rating": 5,
            "availability": "In stock",
            "url": "https://example.com/c",
        },
    ]

    analyzer = BookAnalyzer(books)

    assert analyzer.minimum_price() == 10.00


def test_maximum_price():
    books = [
        {
            "title": "Book A",
            "price": 20.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://example.com/a",
        },
        {
            "title": "Book B",
            "price": 10.00,
            "rating": 4,
            "availability": "In stock",
            "url": "https://example.com/b",
        },
        {
            "title": "Book C",
            "price": 30.00,
            "rating": 5,
            "availability": "In stock",
            "url": "https://example.com/c",
        },
    ]

    analyzer = BookAnalyzer(books)

    assert analyzer.maximum_price() == 30.00


def test_median_price_odd():
    books = [
        {
            "title": "Book A",
            "price": 10.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://example.com/a",
        },
        {
            "title": "Book B",
            "price": 20.00,
            "rating": 4,
            "availability": "In stock",
            "url": "https://example.com/b",
        },
        {
            "title": "Book C",
            "price": 30.00,
            "rating": 5,
            "availability": "In stock",
            "url": "https://example.com/c",
        },
    ]

    analyzer = BookAnalyzer(books)

    assert analyzer.median_price() == 20.00


def test_median_price_even():
    books = [
        {
            "title": "Book A",
            "price": 10.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://example.com/a",
        },
        {
            "title": "Book B",
            "price": 20.00,
            "rating": 4,
            "availability": "In stock",
            "url": "https://example.com/b",
        },
        {
            "title": "Book C",
            "price": 30.00,
            "rating": 5,
            "availability": "In stock",
            "url": "https://example.com/c",
        },
        {
            "title": "Book D",
            "price": 40.00,
            "rating": 2,
            "availability": "In stock",
            "url": "https://example.com/d",
        },
    ]

    analyzer = BookAnalyzer(books)

    assert analyzer.median_price() == 25.00

def test_price_range():
    books = [
        {
            "title": "Book A",
            "price": 10.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://example.com/book-a",
        },
        {
            "title": "Book B",
            "price": 50.00,
            "rating": 5,
            "availability": "In stock",
            "url": "https://example.com/book-b",
        },
    ]

    analyzer = BookAnalyzer(books)

    assert analyzer.price_range() == 40.00
def test_books_by_rating():
    books = [
        {
            "title": "Book A",
            "price": 10.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://example.com/book-a",
        },
        {
            "title": "Book B",
            "price": 20.00,
            "rating": 5,
            "availability": "In stock",
            "url": "https://example.com/book-b",
        },
        {
            "title": "Book C",
            "price": 30.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://example.com/book-c",
        },
    ]

    analyzer = BookAnalyzer(books)

    groups = analyzer.books_by_rating()

    assert len(groups[3]) == 2
    assert len(groups[5]) == 1
    assert len(groups[1]) == 0