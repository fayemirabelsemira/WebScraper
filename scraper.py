import argparse
import sys
import json
import csv
from pathlib import Path

from src.scraper.main import main as scraper_main
from src.scraper.database import BookDatabase
from src.scraper.analyzer import BookAnalyzer
from src.scraper.report_generator import generate_report


# ==========================================
# DEFAULT PATHS
# ==========================================

DEFAULT_JSON = "data/books.json"
DEFAULT_CSV = "data/books.csv"
DEFAULT_REPORT = "reports/scraper_report.txt"


# ==========================================
# LOAD BOOKS FROM JSON
# ==========================================

def load_books_from_json(file_path):
    """Load books from a JSON file."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"JSON file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==========================================
# LOAD BOOKS FROM CSV
# ==========================================

def load_books_from_csv(file_path):
    """Load books from a CSV file."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {path}"
        )

    books = []

    with path.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            books.append(
                {
                    "title": row["title"],
                    "price": float(row["price"]),
                    "rating": int(row["rating"]),
                    "availability": row["availability"],
                    "url": row["url"],
                }
            )

    return books


# ==========================================
# LOAD SCRAPED BOOK DATA
# ==========================================

def load_books(file_path=None):
    """Load scraped books from JSON or CSV."""

    if file_path:

        path = Path(file_path)

        if path.suffix.lower() == ".json":
            return load_books_from_json(path)

        if path.suffix.lower() == ".csv":
            return load_books_from_csv(path)

        raise ValueError(
            "Input file must be .json or .csv"
        )

    # Prefer JSON
    json_path = Path(DEFAULT_JSON)

    if json_path.exists():

        return load_books_from_json(
            json_path
        )

    # Fall back to CSV
    csv_path = Path(DEFAULT_CSV)

    if csv_path.exists():

        return load_books_from_csv(
            csv_path
        )

    raise FileNotFoundError(
        "No scraped data found. "
        "Run the scrape command first."
    )


# ==========================================
# ANALYZE COMMAND
# ==========================================

def run_analyze(file_path=None):
    """Analyze scraped book data."""

    try:

        books = load_books(file_path)

    except (
        FileNotFoundError,
        ValueError,
        json.JSONDecodeError
    ) as error:

        print(
            f"\nAnalyze error: {error}"
        )

        return

    analyzer = BookAnalyzer(books)

    print()
    print("=" * 50)
    print("              BOOK ANALYSIS")
    print("=" * 50)

    print()

    print("BASIC STATISTICS")
    print("-" * 50)

    print(
        f"Total books: "
        f"{analyzer.total_books()}"
    )

    print(
        f"Average price: "
        f"£{analyzer.average_price():.2f}"
    )

    print(
        f"Average rating: "
        f"{analyzer.average_rating():.2f}"
    )

    print()

    print("PRICE STATISTICS")
    print("-" * 50)

    print(
        f"Minimum price: "
        f"£{analyzer.minimum_price():.2f}"
    )

    print(
        f"Maximum price: "
        f"£{analyzer.maximum_price():.2f}"
    )

    print(
        f"Median price: "
        f"£{analyzer.median_price():.2f}"
    )

    print(
        f"Price range: "
        f"£{analyzer.price_range():.2f}"
    )

    most_expensive = analyzer.most_expensive()

    if most_expensive:

        print(
            f"Most expensive: "
            f"{most_expensive['title']} "
            f"(£{most_expensive['price']:.2f})"
        )

    cheapest = analyzer.cheapest()

    if cheapest:

        print(
            f"Cheapest: "
            f"{cheapest['title']} "
            f"(£{cheapest['price']:.2f})"
        )

    print()

    print("RATING STATISTICS")
    print("-" * 50)

    rating_counts = analyzer.rating_counts()

    for rating in range(1, 6):

        count = rating_counts.get(
            rating,
            0
        )

        if rating == 1:

            print(
                f"{rating} star: {count}"
            )

        else:

            print(
                f"{rating} stars: {count}"
            )

    most_common = analyzer.most_common_rating()

    if most_common is not None:

        print(
            f"\nMost common rating: "
            f"{most_common} stars"
        )

    print()

    print("AVAILABILITY")
    print("-" * 50)

    availability_counts = (
        analyzer.availability_counts()
    )

    for availability, count in (
        availability_counts.items()
    ):

        print(
            f"{availability}: {count}"
        )

    print()

    print("AVERAGE PRICE BY RATING")
    print("-" * 50)

    averages = (
        analyzer.average_price_by_rating()
    )

    for rating, average in averages.items():

        if average > 0:

            print(
                f"{rating} star: "
                f"£{average:.2f}"
            )

        else:

            print(
                f"{rating} star: "
                f"No books"
            )

    print()

    print("=" * 50)
    print("             ANALYSIS COMPLETE")
    print("=" * 50)


# ==========================================
# REPORT COMMAND
# ==========================================

def run_report(
    file_path=None,
    output_path=DEFAULT_REPORT
):
    """Generate a report from scraped data."""

    try:

        books = load_books(file_path)

    except (
        FileNotFoundError,
        ValueError,
        json.JSONDecodeError
    ) as error:

        print(
            f"\nReport error: {error}"
        )

        return

    print()
    print("Generating report...")

    generate_report(
        books,
        output_path
    )

    print(
        f"Report saved to: "
        f"{output_path}"
    )


# ==========================================
# DATABASE COMMAND
# ==========================================

def run_database(args):
    """Run database operations."""

    database = BookDatabase()

    try:

        # ==================================
        # DASHBOARD
        # ==================================

        if args.dashboard:

            database.print_database_dashboard()

            return

        # ==================================
        # PRICE STATISTICS
        # ==================================

        if args.stats:

            statistics = (
                database.get_price_statistics()
            )

            print()
            print("=" * 50)
            print("       DATABASE PRICE STATISTICS")
            print("=" * 50)

            print(
                f"Minimum price: "
                f"£{statistics['minimum']:.2f}"
            )

            print(
                f"Maximum price: "
                f"£{statistics['maximum']:.2f}"
            )

            print(
                f"Average price: "
                f"£{statistics['average']:.2f}"
            )

            print("=" * 50)

            return

        # ==================================
        # RATING STATISTICS
        # ==================================

        if args.rating_stats:

            rating_counts = (
                database.get_rating_counts()
            )

            print()
            print("=" * 50)
            print("        DATABASE RATING STATISTICS")
            print("=" * 50)

            for rating in range(1, 6):

                count = rating_counts.get(
                    rating,
                    0
                )

                if rating == 1:

                    print(
                        f"{rating} star: {count}"
                    )

                else:

                    print(
                        f"{rating} stars: {count}"
                    )

            print("=" * 50)

            return

        # ==================================
        # EXPORT DATABASE
        # ==================================

        if args.export_db:

            output_path = (
                database.export_to_csv()
            )

            print()
            print("=" * 50)
            print("           DATABASE EXPORT")
            print("=" * 50)

            print(
                f"Books exported: "
                f"{database.count_books()}"
            )

            print(
                f"CSV file: "
                f"{output_path}"
            )

            print("=" * 50)

            return

        # ==================================
        # IMPORT DATABASE
        # ==================================

        if args.import_db:

            try:

                imported_count = (
                    database.import_from_csv(
                        args.import_db
                    )
                )

                print()
                print("=" * 50)
                print("           DATABASE IMPORT")
                print("=" * 50)

                print(
                    f"Books imported: "
                    f"{imported_count}"
                )

                print(
                    f"CSV file: "
                    f"{args.import_db}"
                )

                print(
                    f"Total books in database: "
                    f"{database.count_books()}"
                )

                print("=" * 50)

            except FileNotFoundError as error:

                print(
                    f"\nImport error: "
                    f"{error}"
                )

            return

        # ==================================
        # DATABASE SEARCH
        # ==================================

        # Pagination and sorting are also
        # database search operations.
        search_requested = (
            args.search
            or args.min_price is not None
            or args.max_price is not None
            or args.rating is not None
            or args.sort != "title"
            or args.descending
            or args.page != 1
            or args.limit != 20
        )

        if search_requested:

            results = database.search_books(
                keyword=args.search,
                min_price=args.min_price,
                max_price=args.max_price,
                rating=args.rating,
                sort_by=args.sort,
                descending=args.descending,
                page=args.page,
                limit=args.limit,
            )

            print()
            print("=" * 50)
            print("             DATABASE SEARCH")
            print("=" * 50)

            if args.search:

                print(
                    f'Search: "{args.search}"'
                )

            if args.min_price is not None:

                print(
                    f"Minimum price: "
                    f"£{args.min_price:.2f}"
                )

            if args.max_price is not None:

                print(
                    f"Maximum price: "
                    f"£{args.max_price:.2f}"
                )

            if args.rating is not None:

                print(
                    f"Rating: "
                    f"{args.rating} stars"
                )

            print(
                f"Sort by: "
                f"{args.sort}"
            )

            if args.descending:

                print(
                    "Sort order: descending"
                )

            else:

                print(
                    "Sort order: ascending"
                )

            print(
                f"Page: "
                f"{args.page}"
            )

            print(
                f"Books per page: "
                f"{args.limit}"
            )

            print(
                f"Books found: "
                f"{len(results)}"
            )

            print("=" * 50)

            if results:

                for number, book in enumerate(
                    results,
                    start=1
                ):

                    print(
                        f"\n{number}. "
                        f"{book['title']}"
                    )

                    print(
                        f"   Price: "
                        f"£{book['price']:.2f}"
                    )

                    print(
                        f"   Rating: "
                        f"{book['rating']} stars"
                    )

                    print(
                        f"   Availability: "
                        f"{book['availability']}"
                    )

                    print(
                        f"   URL: "
                        f"{book['url']}"
                    )

            else:

                print(
                    "\nNo books found."
                )

            return

        # ==================================
        # DEFAULT DATABASE INFORMATION
        # ==================================

        summary = (
            database.get_database_summary()
        )

        print()
        print("=" * 50)
        print("          DATABASE INFORMATION")
        print("=" * 50)

        print(
            f"Total books: "
            f"{summary['total_books']}"
        )

        print(
            f"Minimum price: "
            f"£{summary['minimum_price']:.2f}"
        )

        print(
            f"Maximum price: "
            f"£{summary['maximum_price']:.2f}"
        )

        print(
            f"Average price: "
            f"£{summary['average_price']:.2f}"
        )

        print("=" * 50)

    finally:

        database.close()


# ==========================================
# MAIN CLI
# ==========================================

def main():

    parser = argparse.ArgumentParser(
        description="WebScraper Command Line Interface"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="WebScraper 1.0"
    )

    # ==========================================
    # OUTPUT OPTIONS
    # ==========================================

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output."
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Show minimal output."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands"
    )

    # ==========================================
    # SCRAPE COMMAND
    # ==========================================

    scrape_parser = subparsers.add_parser(
        "scrape",
        help="Scrape books from the website"
    )

    scrape_parser.add_argument(
        "--url",
        default="https://books.toscrape.com/",
        help="Starting URL to scrape"
    )

    scrape_parser.add_argument(
        "--output",
        default="data/books",
        help="Output file path without extension"
    )

    scrape_parser.add_argument(
        "--format",
        choices=["csv", "json", "both"],
        default="both",
        help="Output format"
    )

    scrape_parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Maximum number of pages to scrape"
    )

    scrape_parser.add_argument(
        "--min-price",
        type=float,
        default=None,
        help="Minimum book price"
    )

    scrape_parser.add_argument(
        "--max-price",
        type=float,
        default=None,
        help="Maximum book price"
    )

    scrape_parser.add_argument(
        "--rating",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=None,
        help="Filter books by rating"
    )

    # ==========================================
    # ANALYZE COMMAND
    # ==========================================

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze scraped book data"
    )

    analyze_parser.add_argument(
        "--input",
        default=None,
        help="Input JSON or CSV file"
    )

    # ==========================================
    # REPORT COMMAND
    # ==========================================

    report_parser = subparsers.add_parser(
        "report",
        help="Generate a scraper report"
    )

    report_parser.add_argument(
        "--input",
        default=None,
        help="Input JSON or CSV file"
    )

    report_parser.add_argument(
        "--output",
        default=DEFAULT_REPORT,
        help="Report output path"
    )

    # ==========================================
    # DATABASE COMMAND
    # ==========================================

    database_parser = subparsers.add_parser(
        "database",
        help="Manage and inspect the SQLite database"
    )

    database_parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Show complete database dashboard"
    )

    database_parser.add_argument(
        "--stats",
        action="store_true",
        help="Show database price statistics"
    )

    database_parser.add_argument(
        "--rating-stats",
        action="store_true",
        help="Show database rating statistics"
    )

    database_parser.add_argument(
        "--search",
        type=str,
        default=None,
        help="Search books by title"
    )

    database_parser.add_argument(
        "--min-price",
        type=float,
        default=None,
        help="Minimum book price"
    )

    database_parser.add_argument(
        "--max-price",
        type=float,
        default=None,
        help="Maximum book price"
    )

    database_parser.add_argument(
        "--rating",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=None,
        help="Filter by rating"
    )

    database_parser.add_argument(
        "--sort",
        choices=["title", "price", "rating"],
        default="title",
        help="Sort results by title, price, or rating"
    )

    database_parser.add_argument(
        "--descending",
        action="store_true",
        help="Sort results in descending order"
    )

    database_parser.add_argument(
        "--page",
        type=int,
        default=1,
        help="Page number"
    )

    database_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of books per page"
    )

    database_parser.add_argument(
        "--export-db",
        action="store_true",
        help="Export database books to CSV"
    )

    database_parser.add_argument(
        "--import-db",
        type=str,
        default=None,
        help="Import books from a CSV file"
    )

    args = parser.parse_args()

    # ==========================================
    # VERBOSE / QUIET VALIDATION
    # ==========================================

    if args.verbose and args.quiet:

        parser.error(
            "--verbose and --quiet cannot be used together."
        )

    # ==========================================
    # SCRAPE
    # ==========================================

    if args.command == "scrape":

        scraper_arguments = [
            "scraper_main"
        ]

        scraper_arguments.extend(
            [
                "--url",
                args.url,
                "--output",
                args.output,
                "--format",
                args.format,
            ]
        )

        if args.max_pages is not None:

            scraper_arguments.extend(
                [
                    "--max-pages",
                    str(args.max_pages),
                ]
            )

        if args.min_price is not None:

            scraper_arguments.extend(
                [
                    "--min-price",
                    str(args.min_price),
                ]
            )

        if args.max_price is not None:

            scraper_arguments.extend(
                [
                    "--max-price",
                    str(args.max_price),
                ]
            )

        if args.rating is not None:

            scraper_arguments.extend(
                [
                    "--rating",
                    str(args.rating),
                ]
            )

        original_arguments = sys.argv

        try:

            sys.argv = scraper_arguments

            scraper_main()

        finally:

            sys.argv = original_arguments

    # ==========================================
    # ANALYZE
    # ==========================================

    elif args.command == "analyze":

        run_analyze(
            args.input
        )

    # ==========================================
    # REPORT
    # ==========================================

    elif args.command == "report":

        run_report(
            args.input,
            args.output
        )

    # ==========================================
    # DATABASE
    # ==========================================

    elif args.command == "database":

        run_database(
            args
        )

    # ==========================================
    # NO COMMAND
    # ==========================================

    else:

        parser.print_help()


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()