import sqlite3
import csv
from pathlib import Path


class BookDatabase:
    """Handles SQLite database operations for books."""

    def __init__(self, database_path="data/books.db"):
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            self.database_path
        )

        self.create_table()

    def create_table(self):
        """Create the books table if it does not exist."""

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL NOT NULL,
                rating INTEGER NOT NULL,
                availability TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE
            )
            """
        )

        self.connection.commit()

    def insert_book(self, book):
        """Insert one book into the database."""

        self.connection.execute(
            """
            INSERT OR IGNORE INTO books
            (title, price, rating, availability, url)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                book["title"],
                book["price"],
                book["rating"],
                book["availability"],
                book["url"],
            )
        )

        self.connection.commit()

    def insert_books(self, books):
        """Insert multiple books into the database."""

        for book in books:
            self.connection.execute(
                """
                INSERT OR IGNORE INTO books
                (title, price, rating, availability, url)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    book["title"],
                    book["price"],
                    book["rating"],
                    book["availability"],
                    book["url"],
                )
            )

        self.connection.commit()

    def get_all_books(self):
        """Return all books from the database."""

        cursor = self.connection.execute(
            """
            SELECT
                id,
                title,
                price,
                rating,
                availability,
                url
            FROM books
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

        books = []

        for row in rows:
            books.append(
                {
                    "id": row[0],
                    "title": row[1],
                    "price": row[2],
                    "rating": row[3],
                    "availability": row[4],
                    "url": row[5],
                }
            )

        return books

    def count_books(self):
        """Return the number of books in the database."""

        cursor = self.connection.execute(
            "SELECT COUNT(*) FROM books"
        )

        return cursor.fetchone()[0]

    def search_books(
        self,
        keyword="",
        min_price=None,
        max_price=None,
        rating=None,
        sort_by="title",
        descending=False,
        page=1,
        limit=20
    ):
        """Search, sort, and paginate books."""

        query = """
            SELECT
                id,
                title,
                price,
                rating,
                availability,
                url
            FROM books
            WHERE 1 = 1
        """

        parameters = []

        # Search by title
        if keyword:
            query += " AND title LIKE ?"

            parameters.append(
                f"%{keyword}%"
            )

        # Minimum price
        if min_price is not None:
            query += " AND price >= ?"

            parameters.append(
                min_price
            )

        # Maximum price
        if max_price is not None:
            query += " AND price <= ?"

            parameters.append(
                max_price
            )

        # Rating
        if rating is not None:
            query += " AND rating = ?"

            parameters.append(
                rating
            )

        # Allowed sorting fields
        sort_columns = {
            "title": "title",
            "price": "price",
            "rating": "rating",
        }

        if sort_by not in sort_columns:
            sort_by = "title"

        order = "DESC" if descending else "ASC"

        query += (
            f" ORDER BY "
            f"{sort_columns[sort_by]} "
            f"{order}"
        )

        # Pagination
        if page < 1:
            page = 1

        if limit < 1:
            limit = 20

        offset = (page - 1) * limit

        query += " LIMIT ? OFFSET ?"

        parameters.append(limit)
        parameters.append(offset)

        cursor = self.connection.execute(
            query,
            parameters
        )

        rows = cursor.fetchall()

        books = []

        for row in rows:
            books.append(
                {
                    "id": row[0],
                    "title": row[1],
                    "price": row[2],
                    "rating": row[3],
                    "availability": row[4],
                    "url": row[5],
                }
            )

        return books

    def close(self):
        """Close the database connection."""

        self.connection.close()

    def get_books_by_price_range(
        self,
        min_price: float,
        max_price: float
    ) -> list[dict]:
        """Return books within a specific price range."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT title, price, rating, availability, url
            FROM books
            WHERE price >= ?
            AND price <= ?
            ORDER BY price ASC
            """,
            (min_price, max_price)
        )

        rows = cursor.fetchall()

        return [
            {
                "title": row[0],
                "price": row[1],
                "rating": row[2],
                "availability": row[3],
                "url": row[4],
            }
            for row in rows
        ]

    def get_price_statistics(self) -> dict:
        """Return basic price statistics from the database."""

        cursor = self.connection.execute(
            """
            SELECT
                MIN(price),
                MAX(price),
                AVG(price)
            FROM books
            """
        )

        row = cursor.fetchone()

        return {
            "minimum": row[0] if row[0] is not None else 0.0,
            "maximum": row[1] if row[1] is not None else 0.0,
            "average": row[2] if row[2] is not None else 0.0,
        }

    def export_to_csv(
        self,
        output_path="data/database_books.csv"
    ):
        """Export all books from the database to a CSV file."""

        books = self.get_all_books()

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        fieldnames = [
            "id",
            "title",
            "price",
            "rating",
            "availability",
            "url",
        ]

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()

            writer.writerows(books)

        return output_path

    def import_from_csv(
        self,
        input_path
    ):
        """Import books from a CSV file into the database."""

        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {input_path}"
            )

        with input_path.open(
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            books = []

            for row in reader:

                # Convert price from formats such as:
                # £10.99
                # 10.99
                price = float(
                    row["price"]
                    .replace("£", "")
                    .strip()
                )

                # Convert rating from words or numbers
                rating_value = row["rating"].strip()

                rating_map = {
                    "One": 1,
                    "Two": 2,
                    "Three": 3,
                    "Four": 4,
                    "Five": 5,
                }

                if rating_value in rating_map:
                    rating = rating_map[rating_value]
                else:
                    rating = int(rating_value)

                # Some CSV files may not contain a URL.
                # Generate a unique placeholder URL.
                url = row.get("url", "").strip()

                if not url:
                    url = (
                        "imported://"
                        + row["title"].strip().replace(" ", "_")
                        + "_"
                        + str(len(books) + 1)
                    )

                book = {
                    "title": row["title"].strip(),
                    "price": price,
                    "rating": rating,
                    "availability": row["availability"].strip(),
                    "url": url,
                }

                books.append(book)

        self.insert_books(books)

        return len(books)

    def get_rating_counts(self) -> dict:
        """Return the number of books for each rating."""

        cursor = self.connection.execute(
            """
            SELECT rating, COUNT(*)
            FROM books
            GROUP BY rating
            ORDER BY rating
            """
        )

        rows = cursor.fetchall()

        return {
            row[0]: row[1]
            for row in rows
        }

    def get_database_summary(self) -> dict:
        """Return a complete summary of the database."""

        price_statistics = self.get_price_statistics()
        rating_counts = self.get_rating_counts()

        return {
            "total_books": self.count_books(),
            "minimum_price": price_statistics["minimum"],
            "maximum_price": price_statistics["maximum"],
            "average_price": price_statistics["average"],
            "rating_counts": rating_counts,
        }

    def print_database_dashboard(self):
        """Print a readable database dashboard."""

        summary = self.get_database_summary()

        print()
        print("=" * 50)
        print("           DATABASE DASHBOARD")
        print("=" * 50)
        print()

        print("BASIC STATISTICS")
        print("-" * 50)

        print(
            f"Total books: "
            f"{summary['total_books']}"
        )

        print()

        print("PRICE STATISTICS")
        print("-" * 50)

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

        print()

        print("RATING STATISTICS")
        print("-" * 50)

        for rating in range(1, 6):
            count = summary["rating_counts"].get(
                rating,
                0
            )

            print(
                f"{rating} star: "
                f"{count}"
            )

        print()

        print("=" * 50)
        print("        DASHBOARD GENERATED")
        print("=" * 50)