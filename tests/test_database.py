from src.scraper.database import BookDatabase


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
]


def test_database_creation(tmp_path):
    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    assert database_path.exists()

    database.close()


def test_insert_book(tmp_path):
    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    database.insert_book(books[0])

    assert database.count_books() == 1

    database.close()


def test_insert_multiple_books(tmp_path):
    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    database.insert_books(books)

    assert database.count_books() == 2

    database.close()


def test_get_all_books(tmp_path):
    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    database.insert_books(books)

    result = database.get_all_books()

    assert len(result) == 2
    assert result[0]["title"] == "Book A"
    assert result[1]["title"] == "Book B"

    database.close()


def test_duplicate_books_are_ignored(tmp_path):
    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    database.insert_book(books[0])
    database.insert_book(books[0])

    assert database.count_books() == 1

    database.close()


def test_search_books(tmp_path):
    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    database.insert_books(books)

    result = database.search_books(
        keyword="Book A"
    )

    assert len(result) == 1
    assert result[0]["title"] == "Book A"

    database.close()


def test_search_books_sorted_by_price(tmp_path):
    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    database.insert_books(books)

    result = database.search_books(
        sort_by="price"
    )

    assert result[0]["title"] == "Book A"
    assert result[1]["title"] == "Book B"

    database.close()


def test_search_books_sorted_by_price_descending(tmp_path):
    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    database.insert_books(books)

    result = database.search_books(
        sort_by="price",
        descending=True
    )

    assert result[0]["title"] == "Book B"
    assert result[1]["title"] == "Book A"

    database.close()


def test_get_books_by_price_range(tmp_path):
    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    test_books = [
        {
            "title": "Cheap Book",
            "price": 10.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://test.example.com/cheap",
        },
        {
            "title": "Middle Book",
            "price": 30.00,
            "rating": 4,
            "availability": "In stock",
            "url": "https://test.example.com/middle",
        },
        {
            "title": "Expensive Book",
            "price": 60.00,
            "rating": 5,
            "availability": "In stock",
            "url": "https://test.example.com/expensive",
        },
    ]

    database.insert_books(test_books)

    results = database.get_books_by_price_range(
        20.00,
        40.00
    )

    titles = [
        book["title"]
        for book in results
    ]

    assert "Middle Book" in titles
    assert "Cheap Book" not in titles
    assert "Expensive Book" not in titles

    database.close()


def test_get_price_statistics(tmp_path):
    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    test_books = [
        {
            "title": "Book A",
            "price": 10.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://test.example.com/a",
        },
        {
            "title": "Book B",
            "price": 20.00,
            "rating": 4,
            "availability": "In stock",
            "url": "https://test.example.com/b",
        },
        {
            "title": "Book C",
            "price": 30.00,
            "rating": 5,
            "availability": "In stock",
            "url": "https://test.example.com/c",
        },
    ]

    database.insert_books(test_books)

    statistics = database.get_price_statistics()

    assert statistics["minimum"] == 10.00
    assert statistics["maximum"] == 30.00
    assert statistics["average"] == 20.00

    database.close()


def test_search_books_pagination(tmp_path):
    """Test database search pagination."""

    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    test_books = []

    for number in range(1, 11):
        test_books.append(
            {
                "title": f"Book {number}",
                "price": float(number * 10),
                "rating": 5,
                "availability": "In stock",
                "url": f"https://example.com/book-{number}",
            }
        )

    database.insert_books(test_books)

    page_one = database.search_books(
        page=1,
        limit=5
    )

    page_two = database.search_books(
        page=2,
        limit=5
    )

    assert len(page_one) == 5
    assert len(page_two) == 5

    page_one_urls = {
        book["url"]
        for book in page_one
    }

    page_two_urls = {
        book["url"]
        for book in page_two
    }

    assert page_one_urls.isdisjoint(
        page_two_urls
    )

    database.close()


def test_search_books_custom_limit(tmp_path):
    """Test custom pagination limit."""

    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    database.insert_books(books)

    results = database.search_books(
        page=1,
        limit=1
    )

    assert len(results) == 1

    database.close()


def test_search_books_second_page(tmp_path):
    """Test retrieving a second page."""

    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    test_books = []

    for number in range(1, 21):
        test_books.append(
            {
                "title": f"Book {number}",
                "price": float(number * 10),
                "rating": 5,
                "availability": "In stock",
                "url": f"https://example.com/book-{number}",
            }
        )

    database.insert_books(test_books)

    page_one = database.search_books(
        page=1,
        limit=10
    )

    page_two = database.search_books(
        page=2,
        limit=10
    )

    assert len(page_one) == 10
    assert len(page_two) == 10

    assert (
        page_one[0]["url"]
        != page_two[0]["url"]
    )

    database.close()


def test_search_books_invalid_page(tmp_path):
    """Test that an invalid page defaults to page 1."""

    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    database.insert_books(books)

    results = database.search_books(
        page=0,
        limit=1
    )

    expected = database.search_books(
        page=1,
        limit=1
    )

    assert results == expected

    database.close()


def test_search_books_invalid_limit(tmp_path):
    """Test that an invalid limit defaults to 20."""

    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    database.insert_books(books)

    results = database.search_books(
        page=1,
        limit=0
    )

    expected = database.search_books(
        page=1,
        limit=20
    )

    assert results == expected

    database.close()


def test_get_database_summary(tmp_path):
    """Test complete database summary."""

    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    test_books = [
        {
            "title": "Book A",
            "price": 10.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://summary.example.com/a",
        },
        {
            "title": "Book B",
            "price": 20.00,
            "rating": 4,
            "availability": "In stock",
            "url": "https://summary.example.com/b",
        },
        {
            "title": "Book C",
            "price": 30.00,
            "rating": 5,
            "availability": "In stock",
            "url": "https://summary.example.com/c",
        },
    ]

    database.insert_books(test_books)

    summary = database.get_database_summary()

    assert summary["total_books"] == 3
    assert summary["minimum_price"] == 10.00
    assert summary["maximum_price"] == 30.00
    assert summary["average_price"] == 20.00

    assert summary["rating_counts"] == {
        3: 1,
        4: 1,
        5: 1,
    }

    database.close()


def test_print_database_dashboard(tmp_path, capsys):
    """Test database dashboard output."""

    database_path = tmp_path / "books.db"

    database = BookDatabase(database_path)

    test_books = [
        {
            "title": "Book A",
            "price": 10.00,
            "rating": 3,
            "availability": "In stock",
            "url": "https://dashboard.example.com/a",
        },
        {
            "title": "Book B",
            "price": 20.00,
            "rating": 4,
            "availability": "In stock",
            "url": "https://dashboard.example.com/b",
        },
        {
            "title": "Book C",
            "price": 30.00,
            "rating": 5,
            "availability": "In stock",
            "url": "https://dashboard.example.com/c",
        },
    ]

    database.insert_books(test_books)

    database.print_database_dashboard()

    captured = capsys.readouterr()

    assert "DATABASE DASHBOARD" in captured.out
    assert "BASIC STATISTICS" in captured.out
    assert "PRICE STATISTICS" in captured.out
    assert "RATING STATISTICS" in captured.out

    assert "Total books: 3" in captured.out
    assert "Minimum price: £10.00" in captured.out
    assert "Maximum price: £30.00" in captured.out
    assert "Average price: £20.00" in captured.out

    assert "1 star: 0" in captured.out
    assert "2 star: 0" in captured.out
    assert "3 star: 1" in captured.out
    assert "4 star: 1" in captured.out
    assert "5 star: 1" in captured.out

    assert "DASHBOARD GENERATED" in captured.out

    database.close()