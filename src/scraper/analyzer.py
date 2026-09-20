class BookAnalyzer:
    """Analyzes cleaned book data."""

    def __init__(self, books: list[dict]):
        self.books = books

    def total_books(self) -> int:
        return len(self.books)

    def average_price(self) -> float:
        if not self.books:
            return 0.0

        total = sum(
            book["price"]
            for book in self.books
        )

        return round(
            total / len(self.books),
            2
        )

    def average_rating(self) -> float:
        if not self.books:
            return 0.0

        total = sum(
            book["rating"]
            for book in self.books
        )

        return round(
            total / len(self.books),
            2
        )

    def most_expensive(self) -> dict | None:
        if not self.books:
            return None

        return max(
            self.books,
            key=lambda book: book["price"]
        )

    def cheapest(self) -> dict | None:
        if not self.books:
            return None

        return min(
            self.books,
            key=lambda book: book["price"]
        )

    def rating_counts(self) -> dict:
        counts = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
        }

        for book in self.books:
            rating = book["rating"]

            if rating in counts:
                counts[rating] += 1

        return counts

    def most_common_rating(self) -> int | None:
        """Return the rating that appears most often."""

        if not self.books:
            return None

        counts = self.rating_counts()

        return max(
            counts,
            key=counts.get
        )

    def availability_counts(self) -> dict:
        """Count books by availability."""

        counts = {}

        for book in self.books:
            availability = book["availability"]

            counts[availability] = (
                counts.get(availability, 0) + 1
            )

        return counts

    def average_price_by_rating(self) -> dict:
        """Calculate average price for each rating."""

        prices = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
        }

        for book in self.books:
            rating = book["rating"]

            if rating in prices:
                prices[rating].append(
                    book["price"]
                )

        averages = {}

        for rating, rating_prices in prices.items():
            if rating_prices:
                averages[rating] = round(
                    sum(rating_prices)
                    / len(rating_prices),
                    2
                )
            else:
                averages[rating] = 0.0

        return averages

    def highest_rated_books(self) -> list[dict]:
        """Return all books with the highest rating."""

        if not self.books:
            return []

        highest_rating = max(
            book["rating"]
            for book in self.books
        )

        return [
            book
            for book in self.books
            if book["rating"] == highest_rating
        ]

    def lowest_rated_books(self) -> list[dict]:
        """Return all books with the lowest rating."""

        if not self.books:
            return []

        lowest_rating = min(
            book["rating"]
            for book in self.books
        )

        return [
            book
            for book in self.books
            if book["rating"] == lowest_rating
        ]

    def minimum_price(self) -> float:
        """Return the minimum book price."""

        if not self.books:
            return 0.0

        return min(
            book["price"]
            for book in self.books
        )

    def maximum_price(self) -> float:
        """Return the maximum book price."""

        if not self.books:
            return 0.0

        return max(
            book["price"]
            for book in self.books
        )

    def median_price(self) -> float:
        """Return the median book price."""

        if not self.books:
            return 0.0

        prices = sorted(
            book["price"]
            for book in self.books
        )

        middle = len(prices) // 2

        if len(prices) % 2 == 0:
            median = (
                prices[middle - 1]
                + prices[middle]
            ) / 2
        else:
            median = prices[middle]

        return round(median, 2)
    def price_range(self) -> float:
        """Return the difference between the highest and lowest prices."""

        if not self.books:
            return 0.0

        return round(
            self.maximum_price()
            - self.minimum_price(),
            2
        )
    def books_by_rating(self) -> dict:
        """Group books by their rating."""

        groups = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
        }

        for book in self.books:
            rating = book["rating"]

            if rating in groups:
                groups[rating].append(book)

        return groups