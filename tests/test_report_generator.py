from pathlib import Path

from src.scraper.report_generator import generate_report


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
        "availability": "Out of stock",
        "url": "https://example.com/book-c",
    },
]


def test_generate_report(tmp_path):
    output_file = (
        tmp_path / "scraper_report.txt"
    )

    generate_report(
        books,
        output_file
    )

    assert output_file.exists()


def test_report_contains_statistics(tmp_path):
    output_file = (
        tmp_path / "scraper_report.txt"
    )

    generate_report(
        books,
        output_file
    )

    report = output_file.read_text(
        encoding="utf-8"
    )

    assert "WEB SCRAPER REPORT" in report
    assert "Total books: 3" in report
    assert "Average price: £20.00" in report
    assert "Average rating: 4.00" in report


def test_report_contains_price_information(tmp_path):
    output_file = (
        tmp_path / "scraper_report.txt"
    )

    generate_report(
        books,
        output_file
    )

    report = output_file.read_text(
        encoding="utf-8"
    )

    assert "Most expensive: Book C" in report
    assert "Cheapest: Book A" in report


def test_report_contains_rating_information(tmp_path):
    output_file = (
        tmp_path / "scraper_report.txt"
    )

    generate_report(
        books,
        output_file
    )

    report = output_file.read_text(
        encoding="utf-8"
    )

    assert "Most common rating: 3 stars" in report
    assert "3 star: 1" in report
    assert "4 star: 1" in report
    assert "5 star: 1" in report


def test_report_contains_availability(tmp_path):
    output_file = (
        tmp_path / "scraper_report.txt"
    )

    generate_report(
        books,
        output_file
    )

    report = output_file.read_text(
        encoding="utf-8"
    )

    assert "In stock: 2" in report
    assert "Out of stock: 1" in report


def test_report_contains_book_lists(tmp_path):
    output_file = (
        tmp_path / "scraper_report.txt"
    )

    generate_report(
        books,
        output_file
    )

    report = output_file.read_text(
        encoding="utf-8"
    )

    assert "HIGHEST-RATED BOOKS" in report
    assert "Book A" in report

    assert "LOWEST-RATED BOOKS" in report
    assert "Book B" in report