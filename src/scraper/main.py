import argparse

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from src.scraper.http_client import HTTPClient
from src.scraper.parser import BookParser
from src.scraper.cleaner import BookDataCleaner
from src.scraper.exporter import export_to_csv
from src.scraper.json_exporter import export_to_json
from src.scraper.logger import get_logger
from src.scraper.database import BookDatabase
from config.settings import (
    TARGET_URL,
    DEFAULT_MAX_PAGES,
    DEFAULT_MIN_PRICE,
    DEFAULT_MAX_PRICE,
    DEFAULT_RATING,
)


# ==========================================
# SCRAPER PIPELINE
# ==========================================

class ScraperPipeline:
    """Coordinates the web scraping pipeline."""

    def __init__(self):
        self.client = HTTPClient()
        self.parser = BookParser()
        self.cleaner = BookDataCleaner()
        self.database = BookDatabase()
        self.logger = get_logger(__name__)

    # ==========================================
    # FETCH PAGE
    # ==========================================

    def fetch_page(
        self,
        url: str
    ) -> str:
        """Fetch HTML from a URL."""

        self.logger.info(
            "Fetching page: %s",
            url
        )

        return self.client.fetch(url)

    # ==========================================
    # PARSE PAGE
    # ==========================================

    def parse_page(
        self,
        html: str,
        base_url: str
    ) -> list[dict]:
        """Parse books from HTML."""

        books = self.parser.parse(
            html,
            base_url
        )

        self.logger.info(
            "Parsed %d books",
            len(books)
        )

        return books

    # ==========================================
    # CLEAN BOOKS
    # ==========================================

    def clean_books(
        self,
        books: list[dict]
    ) -> list[dict]:
        """Clean and validate book records."""

        cleaned_books = self.cleaner.clean_many(
            books
        )

        self.logger.info(
            "Cleaned %d books",
            len(cleaned_books)
        )

        return cleaned_books

    # ==========================================
    # SAVE TO DATABASE
    # ==========================================

    def save_to_database(
        self,
        books: list[dict]
    ):
        """Save cleaned books to SQLite."""

        if not books:
            return

        self.database.insert_books(
            books
        )

        self.logger.info(
            "Saved %d books to database",
            len(books)
        )

    # ==========================================
    # FIND NEXT PAGE
    # ==========================================

    @staticmethod
    def get_next_url(
        html: str,
        current_url: str
    ) -> str | None:
        """Find the next page URL."""

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        next_link = soup.select_one(
            "li.next a"
        )

        if not next_link:
            return None

        next_href = next_link.get(
            "href"
        )

        if not next_href:
            return None

        return urljoin(
            current_url,
            next_href
        )

    # ==========================================
    # SCRAPE ALL PAGES
    # ==========================================

    def scrape(
        self,
        start_url: str,
        max_pages: int | None = None
    ) -> list[dict]:
        """Run the complete scraping pipeline."""

        all_books = []

        current_url = start_url

        page_number = 1

        while current_url:

            if (
                max_pages is not None
                and page_number > max_pages
            ):
                self.logger.info(
                    "Maximum page limit reached: %d",
                    max_pages
                )

                break

            self.logger.info(
                "Processing page %d: %s",
                page_number,
                current_url
            )

            try:

                # --------------------------
                # FETCH
                # --------------------------

                html = self.fetch_page(
                    current_url
                )

                # --------------------------
                # PARSE
                # --------------------------

                books = self.parse_page(
                    html,
                    current_url
                )

                # --------------------------
                # CLEAN
                # --------------------------

                cleaned_books = self.clean_books(
                    books
                )

                # --------------------------
                # SAVE
                # --------------------------

                self.save_to_database(
                    cleaned_books
                )

                # --------------------------
                # COLLECT
                # --------------------------

                all_books.extend(
                    cleaned_books
                )

                # --------------------------
                # NEXT PAGE
                # --------------------------

                next_url = self.get_next_url(
                    html,
                    current_url
                )

                if not next_url:

                    self.logger.info(
                        "No next page found."
                    )

                    break

                current_url = next_url

                page_number += 1

            except Exception as error:

                self.logger.exception(
                    "Error processing page %d: %s",
                    page_number,
                    error
                )

                break

        self.logger.info(
            "Scraping completed. "
            "Collected %d books.",
            len(all_books)
        )

        return all_books

    # ==========================================
    # CLOSE RESOURCES
    # ==========================================

    def close(self):
        """Close HTTP and database resources."""

        self.client.close()

        self.database.close()


# ==========================================
# FILTER BOOKS
# ==========================================

def filter_books(
    books: list[dict],
    min_price=None,
    max_price=None,
    rating=None
) -> list[dict]:
    """Filter books by price and rating."""

    filtered_books = []

    for book in books:

        if (
            min_price is not None
            and book["price"] < min_price
        ):
            continue

        if (
            max_price is not None
            and book["price"] > max_price
        ):
            continue

        if (
            rating is not None
            and book["rating"] != rating
        ):
            continue

        filtered_books.append(
            book
        )

    return filtered_books


# ==========================================
# REMOVE DUPLICATES
# ==========================================

def remove_duplicates(
    books: list[dict]
) -> list[dict]:
    """Remove duplicate books using their URLs."""

    unique_books = {}

    for book in books:

        url = book.get(
            "url"
        )

        if url:
            unique_books[url] = book

    return list(
        unique_books.values()
    )


# ==========================================
# EXPORT BOOKS
# ==========================================

def export_books(
    books: list[dict],
    output_path: str,
    output_format: str
):
    """Export books to CSV, JSON, or both."""

    if output_format in (
        "csv",
        "both",
    ):

        csv_path = (
            f"{output_path}.csv"
        )

        export_to_csv(
            books,
            csv_path
        )

    if output_format in (
        "json",
        "both",
    ):

        json_path = (
            f"{output_path}.json"
        )

        export_to_json(
            books,
            json_path
        )


# ==========================================
# COMMAND-LINE INTERFACE
# ==========================================

def main():

    command_parser = argparse.ArgumentParser(
        description="Web scraper for Books to Scrape"
    )

    command_parser.add_argument(
        "--url",
        default=TARGET_URL,
        help="Starting URL to scrape",
    )

    command_parser.add_argument(
        "--output",
        default="data/books",
        help="Output file path without extension",
    )

    command_parser.add_argument(
        "--format",
        choices=["csv", "json", "both"],
        default="both",
        help="Output format: csv, json, or both",
    )

    command_parser.add_argument(
        "--max-pages",
        type=int,
        default=DEFAULT_MAX_PAGES,
        help="Maximum number of pages to scrape",
    )

    command_parser.add_argument(
        "--min-price",
        type=float,
        default=DEFAULT_MIN_PRICE,
        help="Minimum book price",
    )

    command_parser.add_argument(
        "--max-price",
        type=float,
        default=DEFAULT_MAX_PRICE,
        help="Maximum book price",
    )

    command_parser.add_argument(
        "--rating",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=DEFAULT_RATING,
        help="Filter books by rating",
    )

    args = command_parser.parse_args()

    # ==========================================
    # VALIDATE ARGUMENTS
    # ==========================================

    if args.max_pages is not None:

        if args.max_pages < 1:

            command_parser.error(
                "--max-pages must be at least 1"
            )

    if (
        args.min_price is not None
        and args.max_price is not None
        and args.min_price > args.max_price
    ):

        command_parser.error(
            "--min-price cannot be greater "
            "than --max-price"
        )

    # ==========================================
    # LOGGER
    # ==========================================

    logger = get_logger(
        __name__
    )

    logger.info(
        "Web scraper started."
    )

    logger.info(
        "Starting URL: %s",
        args.url
    )

    logger.info(
        "Maximum pages: %s",
        args.max_pages
    )

    # ==========================================
    # PIPELINE
    # ==========================================

    pipeline = ScraperPipeline()

    try:

        print(
            "Starting Web Scraper..."
        )

        print(
            f"Starting URL: "
            f"{args.url}"
        )

        if args.max_pages is not None:

            print(
                f"Maximum pages: "
                f"{args.max_pages}"
            )

        print(
            f"Output format: "
            f"{args.format}"
        )

        # ======================================
        # SCRAPE
        # ======================================

        all_books = pipeline.scrape(
            start_url=args.url,
            max_pages=args.max_pages
        )

        # ======================================
        # FILTER
        # ======================================

        filtered_books = filter_books(
            all_books,
            min_price=args.min_price,
            max_price=args.max_price,
            rating=args.rating
        )

        # ======================================
        # REMOVE DUPLICATES
        # ======================================

        filtered_books = remove_duplicates(
            filtered_books
        )

        # ======================================
        # EXPORT
        # ======================================

        export_books(
            filtered_books,
            args.output,
            args.format
        )

        # ======================================
        # EXPORT MESSAGES
        # ======================================

        if args.format in (
            "csv",
            "both",
        ):

            print(
                f"\nCSV saved to: "
                f"{args.output}.csv"
            )

        if args.format in (
            "json",
            "both",
        ):

            print(
                f"JSON saved to: "
                f"{args.output}.json"
            )

        # ======================================
        # SUMMARY
        # ======================================

        print(
            "\n========== SCRAPING SUMMARY =========="
        )

        print(
            f"Books collected: "
            f"{len(all_books)}"
        )

        print(
            f"Books after filtering: "
            f"{len(filtered_books)}"
        )

        print(
            "======================================"
        )

        logger.info(
            "Books collected: %d",
            len(all_books)
        )

        logger.info(
            "Books after filtering: %d",
            len(filtered_books)
        )

        logger.info(
            "Web scraper completed successfully."
        )

    except Exception as error:

        logger.exception(
            "Web scraper failed: %s",
            error
        )

        print(
            f"\nScraper error: {error}"
        )

    finally:

        pipeline.close()


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()