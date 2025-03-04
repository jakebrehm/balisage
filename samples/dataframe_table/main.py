"""
Creates a sample HTML page with some text and a table.
"""

import os
import sys

dir_name = os.path.dirname(__file__)
src_path = os.path.abspath(os.path.join(dir_name, "../../src"))
sys.path.append(src_path)

import pandas as pd  # noqa: E402

from balisage import Classes, Heading1, Page, Paragraph, Table  # noqa: E402


def main() -> None:
    """The main function."""

    # Create example dataframe
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})

    # Create the page
    page = Page(title="DataFrame Table", stylesheets=["./style.css"])

    # Add a horizontal rule and some text
    page.add(
        Heading1("Heading 1", classes=Classes("title")),
        Paragraph("This is a sample dataframe table."),
    )

    # Add a table
    table = Table.from_df(df, table_classes=Classes("top-spacing"))
    page.add(table)

    # Save the page
    filepath = os.path.join(os.path.dirname(__file__), "index.html")
    page.save(filepath, prettify=True)


if __name__ == "__main__":
    main()
