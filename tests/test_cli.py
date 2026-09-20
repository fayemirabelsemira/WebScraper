import subprocess
import sys
from pathlib import Path


def run_cli(*arguments):
    """Run the scraper CLI and return the result."""

    command = [
        sys.executable,
        "scraper.py",
        *arguments,
    ]

    return subprocess.run(
        command,
        capture_output=True,
        text=True,
    )


# ==========================================
# BASIC CLI TESTS
# ==========================================

def test_cli_help():
    """Test the CLI help command."""

    result = run_cli(
        "--help"
    )

    assert result.returncode == 0

    assert (
        "WebScraper Command Line Interface"
        in result.stdout
    )

    assert "scrape" in result.stdout
    assert "analyze" in result.stdout
    assert "report" in result.stdout
    assert "database" in result.stdout


def test_cli_version():
    """Test the CLI version command."""

    result = run_cli(
        "--version"
    )

    assert result.returncode == 0

    assert "WebScraper 1.0" in result.stdout


def test_cli_no_command():
    """Test running the CLI without a command."""

    result = run_cli()

    assert result.returncode == 0

    assert (
        "WebScraper Command Line Interface"
        in result.stdout
    )

    assert "Available commands" in result.stdout


# ==========================================
# SCRAPE CLI TESTS
# ==========================================

def test_cli_scrape_help():
    """Test scrape command help."""

    result = run_cli(
        "scrape",
        "--help"
    )

    assert result.returncode == 0

    assert "--url" in result.stdout
    assert "--output" in result.stdout
    assert "--format" in result.stdout
    assert "--max-pages" in result.stdout
    assert "--min-price" in result.stdout
    assert "--max-price" in result.stdout
    assert "--rating" in result.stdout


# ==========================================
# DATABASE BASIC TESTS
# ==========================================

def test_cli_database():
    """Test the database command."""

    result = run_cli(
        "database"
    )

    assert result.returncode == 0

    assert (
        "DATABASE INFORMATION"
        in result.stdout
    )

    assert "Total books:" in result.stdout


def test_cli_database_dashboard():
    """Test the database dashboard command."""

    result = run_cli(
        "database",
        "--dashboard"
    )

    assert result.returncode == 0

    assert (
        "DATABASE DASHBOARD"
        in result.stdout
    )

    assert "BASIC STATISTICS" in result.stdout
    assert "PRICE STATISTICS" in result.stdout
    assert "RATING STATISTICS" in result.stdout
    assert "Total books:" in result.stdout


def test_cli_database_stats():
    """Test the database price statistics command."""

    result = run_cli(
        "database",
        "--stats"
    )

    assert result.returncode == 0

    assert (
        "DATABASE PRICE STATISTICS"
        in result.stdout
    )

    assert "Minimum price:" in result.stdout
    assert "Maximum price:" in result.stdout
    assert "Average price:" in result.stdout


def test_cli_database_rating_stats():
    """Test the database rating statistics command."""

    result = run_cli(
        "database",
        "--rating-stats"
    )

    assert result.returncode == 0

    assert (
        "DATABASE RATING STATISTICS"
        in result.stdout
    )

    assert "1 star:" in result.stdout
    assert "2 stars:" in result.stdout
    assert "3 stars:" in result.stdout
    assert "4 stars:" in result.stdout
    assert "5 stars:" in result.stdout


# ==========================================
# ANALYZE CLI TESTS
# ==========================================

def test_cli_analyze():
    """Test the analyze command."""

    result = run_cli(
        "analyze"
    )

    assert result.returncode == 0

    assert "BOOK ANALYSIS" in result.stdout
    assert "BASIC STATISTICS" in result.stdout
    assert "PRICE STATISTICS" in result.stdout
    assert "RATING STATISTICS" in result.stdout
    assert "ANALYSIS COMPLETE" in result.stdout


def test_cli_analyze_with_json_input():
    """Test analyze command with a JSON input file."""

    result = run_cli(
        "analyze",
        "--input",
        "data/books.json"
    )

    assert result.returncode == 0

    assert "BOOK ANALYSIS" in result.stdout
    assert "Total books:" in result.stdout
    assert "ANALYSIS COMPLETE" in result.stdout


# ==========================================
# REPORT CLI TESTS
# ==========================================

def test_cli_report():
    """Test the report command."""

    result = run_cli(
        "report"
    )

    assert result.returncode == 0

    assert "Generating report..." in result.stdout
    assert "Report saved to:" in result.stdout


def test_cli_report_with_json_input():
    """Test report command with a JSON input file."""

    result = run_cli(
        "report",
        "--input",
        "data/books.json"
    )

    assert result.returncode == 0

    assert "Generating report..." in result.stdout
    assert "Report saved to:" in result.stdout


def test_cli_report_custom_output():
    """Test report command with a custom output path."""

    output_path = (
        "reports/test_cli_custom_report.txt"
    )

    result = run_cli(
        "report",
        "--output",
        output_path
    )

    assert result.returncode == 0

    assert "Generating report..." in result.stdout
    assert output_path in result.stdout

    assert Path(output_path).exists()

    Path(output_path).unlink()


# ==========================================
# DATABASE SEARCH TESTS
# ==========================================

def test_cli_database_search():
    """Test the database search command."""

    result = run_cli(
        "database",
        "--search",
        "Book"
    )

    assert result.returncode == 0

    assert (
        "DATABASE SEARCH"
        in result.stdout
    )

    assert "Search:" in result.stdout
    assert "Books found:" in result.stdout


def test_cli_database_price_filter():
    """Test database price filtering."""

    result = run_cli(
        "database",
        "--min-price",
        "20",
        "--max-price",
        "40"
    )

    assert result.returncode == 0

    assert (
        "DATABASE SEARCH"
        in result.stdout
    )

    assert "Minimum price: £20.00" in result.stdout
    assert "Maximum price: £40.00" in result.stdout


def test_cli_database_rating_filter():
    """Test database rating filtering."""

    result = run_cli(
        "database",
        "--rating",
        "5"
    )

    assert result.returncode == 0

    assert (
        "DATABASE SEARCH"
        in result.stdout
    )

    assert "Rating: 5 stars" in result.stdout


def test_cli_database_pagination():
    """Test database pagination options."""

    result = run_cli(
        "database",
        "--page",
        "2",
        "--limit",
        "5"
    )

    assert result.returncode == 0

    assert (
        "DATABASE SEARCH"
        in result.stdout
    )

    assert "Page: 2" in result.stdout
    assert "Books per page: 5" in result.stdout
    assert "Books found:" in result.stdout


def test_cli_database_sorting():
    """Test database sorting options."""

    result = run_cli(
        "database",
        "--sort",
        "price",
        "--descending"
    )

    assert result.returncode == 0

    assert (
        "DATABASE SEARCH"
        in result.stdout
    )

    assert "Sort by: price" in result.stdout
    assert "Sort order: descending" in result.stdout


def test_cli_database_rating_sorting():
    """Test database sorting by rating."""

    result = run_cli(
        "database",
        "--sort",
        "rating"
    )

    assert result.returncode == 0

    assert (
        "DATABASE SEARCH"
        in result.stdout
    )

    assert "Sort by: rating" in result.stdout
    assert "Sort order: ascending" in result.stdout


def test_cli_database_combined_filters():
    """Test multiple database filters together."""

    result = run_cli(
        "database",
        "--search",
        "Book",
        "--min-price",
        "20",
        "--max-price",
        "50",
        "--rating",
        "5",
        "--sort",
        "price",
        "--descending",
        "--page",
        "1",
        "--limit",
        "5"
    )

    assert result.returncode == 0

    assert (
        "DATABASE SEARCH"
        in result.stdout
    )

    assert 'Search: "Book"' in result.stdout
    assert "Minimum price: £20.00" in result.stdout
    assert "Maximum price: £50.00" in result.stdout
    assert "Rating: 5 stars" in result.stdout
    assert "Sort by: price" in result.stdout
    assert "Sort order: descending" in result.stdout
    assert "Page: 1" in result.stdout
    assert "Books per page: 5" in result.stdout


# ==========================================
# DATABASE EXPORT / IMPORT TESTS
# ==========================================

def test_cli_database_export():
    """Test exporting database books to CSV."""

    output_path = Path(
        "data/database_books.csv"
    )

    if output_path.exists():
        output_path.unlink()

    result = run_cli(
        "database",
        "--export-db"
    )

    assert result.returncode == 0

    assert "DATABASE EXPORT" in result.stdout
    assert "Books exported:" in result.stdout
    assert "CSV file:" in result.stdout

    assert output_path.exists()


def test_cli_database_import():
    """Test importing books into the database."""

    input_path = Path(
        "data/test_books.csv"
    )

    assert input_path.exists()

    result = run_cli(
        "database",
        "--import-db",
        str(input_path)
    )

    assert result.returncode == 0

    assert "DATABASE IMPORT" in result.stdout
    assert "Books imported:" in result.stdout
    assert "CSV file:" in result.stdout
    assert "Total books in database:" in result.stdout