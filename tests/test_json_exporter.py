import json

from src.scraper.json_exporter import export_to_json


books = [
    {
        "title": "Test Book 1",
        "price": 25.50,
        "rating": 5,
        "availability": "In stock",
        "url": "https://example.com/book-1",
    },
    {
        "title": "Test Book 2",
        "price": 15.75,
        "rating": 3,
        "availability": "In stock",
        "url": "https://example.com/book-2",
    },
]


def test_export_json(tmp_path):
    output_file = tmp_path / "test_books.json"

    export_to_json(
        books,
        output_file
    )

    assert output_file.exists()


def test_json_data(tmp_path):
    output_file = tmp_path / "test_books.json"

    export_to_json(
        books,
        output_file
    )

    with output_file.open(
        "r",
        encoding="utf-8"
    ) as file:

        loaded_books = json.load(file)

    assert loaded_books == books


def test_json_book_count(tmp_path):
    output_file = tmp_path / "test_books.json"

    export_to_json(
        books,
        output_file
    )

    with output_file.open(
        "r",
        encoding="utf-8"
    ) as file:

        loaded_books = json.load(file)

    assert len(loaded_books) == 2


def test_empty_books(tmp_path):
    output_file = tmp_path / "empty.json"

    export_to_json(
        [],
        output_file
    )

    assert not output_file.exists()