import re


class BookDataCleaner:
    """Cleans and validates scraped book records."""

    REQUIRED_FIELDS = {
        "title",
        "price",
        "rating",
        "availability",
        "url",
    }

    def clean(self, book: dict) -> dict | None:
        """Clean and validate a single book record."""

        if not self._has_required_fields(book):
            return None

        cleaned_book = {
            "title": self._clean_title(book["title"]),
            "price": self._clean_price(book["price"]),
            "rating": self._clean_rating(book["rating"]),
            "availability": self._clean_availability(
                book["availability"]
            ),
            "url": book["url"].strip(),
        }

        if not self._is_valid(cleaned_book):
            return None

        return cleaned_book

    def clean_many(self, books: list[dict]) -> list[dict]:
        """Clean multiple book records."""

        cleaned_books = []

        for book in books:
            cleaned_book = self.clean(book)

            if cleaned_book:
                cleaned_books.append(cleaned_book)

        return cleaned_books

    def _has_required_fields(self, book: dict) -> bool:
        """Check whether all required fields exist."""

        return self.REQUIRED_FIELDS.issubset(book.keys())

    @staticmethod
    def _clean_title(title: str) -> str:
        """Normalize whitespace in a book title."""

        return " ".join(title.split())

    @staticmethod
    def _clean_price(price) -> float | None:
        """Ensure price is stored as a positive number."""

        if price is None:
            return None

        try:
            numeric_price = float(price)

            if numeric_price < 0:
                return None

            return round(numeric_price, 2)

        except (TypeError, ValueError):
            return None

    @staticmethod
    def _clean_rating(rating) -> int | None:
        """Validate book rating."""

        if rating is None:
            return None

        try:
            numeric_rating = int(rating)

            if 1 <= numeric_rating <= 5:
                return numeric_rating

        except (TypeError, ValueError):
            pass

        return None

    @staticmethod
    def _clean_availability(availability: str) -> str:
        """Normalize availability text."""

        if not availability:
            return "Unknown"

        return " ".join(availability.split())

    @staticmethod
    def _is_valid(book: dict) -> bool:
        """Perform final validation."""

        if not book["title"]:
            return False

        if not book["url"]:
            return False

        if book["price"] is None:
            return False

        if book["rating"] is None:
            return False

        return bool(
            re.match(
                r"^https?://",
                book["url"],
            )
        )