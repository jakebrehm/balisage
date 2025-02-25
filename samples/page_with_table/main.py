"""
Creates a sample HTML page with an image, text, and table.
"""

import os
import sys

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
sys.path.append(src_path)

import pandas as pd  # noqa: E402

from balisage import (  # noqa: E402
    Attributes,
    Classes,
    Div,
    Heading1,
    Heading2,
    Heading3,
    HorizontalRule,
    Image,
    Page,
    Paragraph,
    Table,
)


def main() -> None:
    """Builds and saves an HTML page with an image, text, and table."""

    # Create example dataframe
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})

    # Create the page
    page = Page(title="Sample Page", stylesheets=["./style.css"])

    # Add a div for the title area
    title_div = Div(classes=Classes("title-area"))
    title_div.add(
        Image(
            classes=Classes("logo"),
            attributes=Attributes({"src": "./logo.svg", "alt": "Logo"}),
        ),
        Heading1("Heading 1", classes=Classes("title")),
        Paragraph("Paragraph 1", classes=Classes("subtitle")),
    )
    page.add(title_div)

    # Add a horizontal rule and some text
    page.add(
        HorizontalRule(),
        Heading2("Heading 2"),
        Heading3("Heading 3"),
        Paragraph("This is a sample paragraph."),
    )

    # Add a table
    table = Table.from_df(df, table_classes=Classes("top-spacing"))
    page.add(table)

    # Save the page
    filepath = os.path.join(os.path.dirname(__file__), "index.html")
    page.save(filepath, prettify=True)


if __name__ == "__main__":
    main()
