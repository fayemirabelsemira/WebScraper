from pathlib import Path

from src.scraper.analyzer import BookAnalyzer


def generate_report(
    books: list[dict],
    output_path="reports/scraper_report.txt"
):
    """Generate a text report from cleaned book data."""

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    analyzer = BookAnalyzer(books)

    lines = []

    # ==========================================
    # REPORT HEADER
    # ==========================================

    lines.append("=" * 50)
    lines.append("           WEB SCRAPER REPORT")
    lines.append("=" * 50)

    lines.append("")

    # ==========================================
    # BASIC STATISTICS
    # ==========================================

    lines.append("BASIC STATISTICS")
    lines.append("-" * 50)

    lines.append(
        f"Total books: {analyzer.total_books()}"
    )

    lines.append(
        f"Average price: £{analyzer.average_price():.2f}"
    )

    lines.append(
        f"Average rating: {analyzer.average_rating():.2f}"
    )

    lines.append("")

    # ==========================================
    # PRICE INFORMATION
    # ==========================================

    lines.append("PRICE INFORMATION")
    lines.append("-" * 50)

    lines.append(
        f"Minimum price: "
        f"£{analyzer.minimum_price():.2f}"
    )

    lines.append(
        f"Maximum price: "
        f"£{analyzer.maximum_price():.2f}"
    )

    lines.append(
        f"Average price: "
        f"£{analyzer.average_price():.2f}"
    )

    lines.append(
        f"Median price: "
        f"£{analyzer.median_price():.2f}"
    )

    lines.append(
        f"Price range: "
        f"£{analyzer.price_range():.2f}"
    )

    most_expensive = analyzer.most_expensive()
    cheapest = analyzer.cheapest()

    if most_expensive:
        lines.append(
            f"Most expensive: "
            f"{most_expensive['title']} "
            f"(£{most_expensive['price']:.2f})"
        )

    if cheapest:
        lines.append(
            f"Cheapest: "
            f"{cheapest['title']} "
            f"(£{cheapest['price']:.2f})"
        )

    lines.append("")

    # ==========================================
    # RATING STATISTICS
    # ==========================================

    lines.append("RATING STATISTICS")
    lines.append("-" * 50)

    most_common = analyzer.most_common_rating()

    if most_common is not None:
        lines.append(
            f"Most common rating: "
            f"{most_common} stars"
        )

    lines.append("")

    lines.append("Rating counts:")

    for rating, count in analyzer.rating_counts().items():
        lines.append(
            f"  {rating} star: {count}"
        )

    lines.append("")

    # ==========================================
    # AVAILABILITY
    # ==========================================

    lines.append("AVAILABILITY")
    lines.append("-" * 50)

    for availability, count in (
        analyzer.availability_counts().items()
    ):
        lines.append(
            f"  {availability}: {count}"
        )

    lines.append("")

    # ==========================================
    # AVERAGE PRICE BY RATING
    # ==========================================

    lines.append("AVERAGE PRICE BY RATING")
    lines.append("-" * 50)

    averages = analyzer.average_price_by_rating()

    for rating, average in averages.items():

        if average > 0:
            lines.append(
                f"  {rating} star: £{average:.2f}"
            )

        else:
            lines.append(
                f"  {rating} star: No books"
            )

    lines.append("")

    # ==========================================
    # BOOKS BY RATING
    # ==========================================

    lines.append("BOOKS BY RATING")
    lines.append("-" * 50)

    books_by_rating = analyzer.books_by_rating()

    for rating, books in books_by_rating.items():
        lines.append(
            f"  {rating} star books: "
            f"{len(books)}"
        )

    lines.append("")

    # ==========================================
    # HIGHEST-RATED BOOKS
    # ==========================================

    lines.append("HIGHEST-RATED BOOKS")
    lines.append("-" * 50)

    highest_rated = analyzer.highest_rated_books()

    for book in highest_rated:
        lines.append(
            f"  • {book['title']} "
            f"(£{book['price']:.2f})"
        )

    lines.append("")

    # ==========================================
    # LOWEST-RATED BOOKS
    # ==========================================

    lines.append("LOWEST-RATED BOOKS")
    lines.append("-" * 50)

    lowest_rated = analyzer.lowest_rated_books()

    for book in lowest_rated:
        lines.append(
            f"  • {book['title']} "
            f"(£{book['price']:.2f})"
        )

    lines.append("")

    # ==========================================
    # REPORT FOOTER
    # ==========================================

    lines.append("=" * 50)
    lines.append("Report generated successfully.")
    lines.append("=" * 50)

    # ==========================================
    # SAVE REPORT
    # ==========================================

    report = "\n".join(lines)

    output_path.write_text(
        report,
        encoding="utf-8"
    )

    print(
        f"Report generated: {output_path}"
    )