"""
Contains code for all top-level HTML classes.
"""

from typing import Any

from ..core import HTMLBuilder


class Page(HTMLBuilder):
    """Constructs an HTML page."""

    def __init__(
        self,
        data: list[Any] | None = None,
        title: str | None = None,
        lang: str = "en",
        charset: str = "UTF-8",
        stylesheets: str | list[str] | None = None,
    ) -> None:
        """Initializes the Page object."""

        # Initialize the builder
        super().__init__(classes=None)
        self.tag = "html"

        # Initialize instance variables
        self._stylesheets: list[str] = []

        # Store instance variables
        self.title = title
        self.lang = lang
        self.charset = charset

        # Add stylesheets
        match stylesheets:
            case str():
                self.add_stylesheet(stylesheets)
            case list():
                self.add_stylesheets(stylesheets)
            case _:
                raise TypeError(
                    "stylesheets argument must be provided as a string "
                    "or list of strings."
                )

        # Set the data
        if data is not None:
            self.set_data(data)

    @property
    def stylesheets(self) -> list[str]:
        """Gets the list of stylesheets."""
        return self._stylesheets

    def add_stylesheet(self, stylesheet: str) -> None:
        """Adds a stylesheet to link."""
        self._stylesheets.append(stylesheet)

    def add_stylesheets(self, stylesheet: list[str]) -> None:
        """Adds stylesheets to link."""
        self._stylesheets.extend(stylesheet)

    def clear_stylesheets(self) -> None:
        """Clears all stylesheets."""
        self._stylesheets.clear()

    def add_data(self, data: Any) -> None:
        """Adds data."""
        self.add_element(data)

    def set_data(self, data: Any | list[Any]) -> None:
        """Sets the data."""
        self.clear_elements()
        if isinstance(data, list):
            self.add_elements(data)
        else:
            self.add_element(data)

    def clear_data(self) -> None:
        """Clears the data."""
        self.clear_elements()

    def add(self, data: Any) -> None:
        """Adds data. Simple wrapper around add_data."""
        self.add_data(data)

    def construct(self) -> str:
        """Generates HTML from the stored elements."""

        # Set up the page
        html = "<!DOCTYPE html>"

        # Open the tag
        html += f"<{self.tag} lang='{self.lang}'>"

        # Add the header
        html += "<head>"
        html += f"<meta charset='{self.charset}'>"
        if self.title:
            html += f"<title>{self.title}</title>"
        for href in self.stylesheets:
            html += f"<link rel='stylesheet' href='{href}'>"
        html += "</head>"

        # Add the data
        html += "<body>"
        for element in self.elements:
            html += f"{element}"
        html += "</body>"

        # Close the tag and return the HTML
        html += f"</{self.tag}>"
        return html
