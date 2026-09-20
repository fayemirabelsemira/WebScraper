import csv
from pathlib import Path


def export_to_csv(books, output_path):
    output_path = Path(output_path)

    # Create the folder if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not books:
        print("No books to export.")
        return

    fieldnames = books[0].keys()

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(books)

    print(f"Exported {len(books)} books to {output_path}")