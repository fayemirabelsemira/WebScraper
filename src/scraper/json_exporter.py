import json
from pathlib import Path


def export_to_json(books, output_path):
    """Export books to a JSON file."""

    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not books:
        print("No books to export.")
        return

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            books,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Exported {len(books)} books to {output_path}"
    )