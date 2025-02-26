"""
Creates a sample HTML page with a image centered within a div.
"""

import os
import sys

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
sys.path.append(src_path)

from balisage import Attributes, Classes, Div, Image, Page  # noqa: E402


def main() -> None:
    """The main function."""

    # Create the page
    page = Page(title="Sample Page", stylesheets=["./style.css"])

    # Add a div for the title area
    title_div = Div(classes=Classes("title-area"))
    title_div.add(
        Image(
            classes=Classes("logo"),
            attributes=Attributes({"src": "./logo.svg", "alt": "Logo"}),
        ),
    )
    page.add(title_div)

    # Save the page
    filepath = os.path.join(os.path.dirname(__file__), "index.html")
    page.save(filepath, prettify=True)


if __name__ == "__main__":
    main()
