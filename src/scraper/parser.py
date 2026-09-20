from bs4 import BeautifulSoup
from urllib.parse import urljoin


class BookParser:
    """Parses book data from Books to Scrape HTML."""

    RATING_MAP = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    def parse(self, html: str, base_url: str) -> list[dict]:
        """Extract all books from a webpage."""

        soup = BeautifulSoup(html, "html.parser")

        books = []

        for article in soup.select("article.product_pod"):
            book = self._parse_book(article, base_url)

            if book:
                books.append(book)

        return books

    def _parse_book(self, article, base_url: str) -> dict | None:
        """Extract information from a single book."""

        title_element = article.select_one("h3 a")

        if not title_element:
            return None

        title = title_element.get("title", "").strip()

        price_element = article.select_one(".price_color")
        price = self._parse_price(price_element)

        rating_element = article.select_one(".star-rating")
        rating = self._parse_rating(rating_element)

        availability_element = article.select_one(".availability")
        availability = self._parse_availability(availability_element)

        relative_url = title_element.get("href", "")
        product_url = urljoin(base_url, relative_url)

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "url": product_url,
        }

    @staticmethod
    def _parse_price(element) -> float | None:
        if not element:
            return None

        text = element.get_text(strip=True)

        try:
            text = text.replace("£", "").replace("Â", "").strip()
            return float(text)
        except ValueError:
            return None

    @classmethod
    def _parse_rating(cls, element) -> int | None:
        """Convert the website's rating text into a number."""

        if not element:
            return None

        classes = element.get("class", [])

        for class_name in classes:
            if class_name in cls.RATING_MAP:
                return cls.RATING_MAP[class_name]

        return None

    @staticmethod
    def _parse_availability(element) -> str:
        """Extract and clean availability information."""

        if not element:
            return "Unknown"

        return element.get_text(" ", strip=True)