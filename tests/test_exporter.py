import csv

from src.scraper.exporter import export_to_csv


def test_export_to_csv(tmp_path):
    books = [
        {
            "title": "Sample Book",
            "price": 10.99,
            "rating": 5,
            "availability": "In stock",
            "url": "https://example.com/sample-book",
        },
        {
            "title": "Another Book",
            "price": 15.50,
            "rating": 4,
            "availability": "In stock",
            "url": "https://example.com/another-book",
        },
    ]

    output_file = tmp_path / "books.csv"

    export_to_csv(books, output_file)

    assert output_file.exists()

    with output_file.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 2
    assert rows[0]["title"] == "Sample Book"
    assert rows[0]["price"] == "10.99"
    assert rows[1]["title"] == "Another Book"