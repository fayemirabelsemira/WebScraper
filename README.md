# Web Scraper

A professional Python web scraper that extracts book information from **Books to Scrape** and processes the data through parsing, cleaning, analysis, database storage, exporting, reporting, and testing.

## Features

- Web scraping using `requests`
- HTML parsing using `BeautifulSoup`
- Automatic data cleaning and validation
- Pagination support
- Price filtering
- Rating filtering
- Duplicate removal
- CSV export
- JSON export
- SQLite database storage
- Database searching
- Database statistics
- Database dashboard
- Database CSV import/export
- Logging system
- Environment variable configuration
- Command-line interface
- Error handling
- Mock-based testing
- Advanced automated testing
- Report generation

---

## Project Structure

```text
WebScraper/
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   ├── books.csv
│   ├── books.json
│   ├── books.db
│   └── database_books.csv
│
├── logs/
│   └── scraper.log
│
├── reports/
│   └── scraper_report.txt
│
├── src/
│   └── scraper/
│       ├── __init__.py
│       ├── analyzer.py
│       ├── cleaner.py
│       ├── database.py
│       ├── exporter.py
│       ├── http_client.py
│       ├── json_exporter.py
│       ├── logger.py
│       ├── main.py
│       ├── parser.py
│       └── report_generator.py
│
├── tests/
│   ├── test_analyzer.py
│   ├── test_clean_many.py
│   ├── test_cleaner.py
│   ├── test_cli.py
│   ├── test_database.py
│   ├── test_error_handling.py
│   ├── test_exporter.py
│   ├── test_json_exporter.py
│   ├── test_logger.py
│   ├── test_pipeline.py
│   └── test_report_generator.py
│
├── scraper.py
├── requirements.txt
├── pyproject.toml
├── pytest.ini
└── README.md
````

---

## Requirements

* Python 3.10 or higher
* Requests
* BeautifulSoup4
* Python-dotenv
* Pytest

---

## Installation

### 1. Clone or download the project

Open the project folder in your terminal.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

The project uses environment variables for configuration.

Create a `.env` file in the project root:

```env
TARGET_URL=https://books.toscrape.com/
REQUEST_TIMEOUT=10
MAX_RETRIES=3
RETRY_BACKOFF_FACTOR=1
LOG_LEVEL=INFO
DEFAULT_MAX_PAGES=50
```

The `.env` file should not be committed to Git.

---

## Running the Scraper

Run the main scraper:

```bash
python3 scraper.py scrape
```

The scraper can also be configured using command-line options.

Example:

```bash
python3 scraper.py scrape --max-pages 5
```

---

## Output Formats

### CSV

```bash
python3 scraper.py scrape --format csv
```

### JSON

```bash
python3 scraper.py scrape --format json
```

### Both CSV and JSON

```bash
python3 scraper.py scrape --format both
```

---

## Filtering

### Filter by minimum price

```bash
python3 scraper.py scrape --min-price 20
```

### Filter by maximum price

```bash
python3 scraper.py scrape --max-price 30
```

### Filter by rating

```bash
python3 scraper.py scrape --rating 5
```

### Combine filters

```bash
python3 scraper.py scrape --min-price 10 --max-price 30 --rating 5
```

---

## Database

### Show database information

```bash
python3 scraper.py database
```

### Show price statistics

```bash
python3 scraper.py database --stats
```

### Show rating statistics

```bash
python3 scraper.py database --rating-stats
```

### Show the complete database dashboard

```bash
python3 scraper.py database --dashboard
```

### Export database records

```bash
python3 scraper.py database --export-db
```

### Import records from CSV

```bash
python3 scraper.py database --import-db data/books.csv
```

---

## Searching the Database

### Search by title

```bash
python3 scraper.py database --search "Python"
```

### Search with a price range

```bash
python3 scraper.py database --min-price 10 --max-price 30
```

### Sort results

```bash
python3 scraper.py database --sort price
```

### Sort in descending order

```bash
python3 scraper.py database --sort price --descending
```

---

## Logging

The scraper uses Python's logging system.

Logs are stored in:

```text
logs/scraper.log
```

The logger supports:

* Console logging
* File logging
* Log levels
* Rotating log files

---

## Testing

### Run all tests

```bash
pytest
```

### Run the pipeline tests

```bash
pytest tests/test_pipeline.py
```

### Run error-handling tests

```bash
pytest tests/test_error_handling.py
```

The project contains automated tests covering:

* Data analysis
* Data cleaning
* Database operations
* CLI behavior
* Error handling
* CSV exporting
* JSON exporting
* Logging
* Scraping pipeline
* Report generation

---

## Technologies Used

* Python
* Requests
* BeautifulSoup
* SQLite
* CSV
* JSON
* Pytest
* Python Logging
* Python-dotenv

---

## Data Source

This project uses:

**Books to Scrape**

```text
https://books.toscrape.com/
```

Books to Scrape is a website designed for practicing web scraping.

---

## Project Goals

This project demonstrates practical Python development skills including:

* Object-oriented programming
* Web scraping
* Data processing
* Data validation
* Database management
* File handling
* HTTP communication
* Error handling
* Automated testing
* Logging
* Configuration management
* Command-line application development
* Python project packaging

---

## Testing Status

The project currently passes the complete automated test suite.

Latest test result:

```text
96 passed in 5.85s
```

---

## License

This project is intended for educational and portfolio purposes.
