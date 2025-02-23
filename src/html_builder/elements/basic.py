"""
Contains code for all top-level HTML classes.
"""

from ..attributes import Element, ElementsType
from ..core import HTMLBuilder


class Page(HTMLBuilder):
    """Constructs an HTML page."""

    def __init__(
        self,
        elements: ElementsType | None = None,
        title: str | None = None,
        lang: str = "en",
        charset: str = "UTF-8",
        stylesheets: list[str] | None = None,
    ) -> None:
        """Initializes the Page object."""

        # Initialize the builder
        super().__init__(
            elements=elements,
            attributes=None,
            classes=None,
        )
        self.tag = "html"

        # Initialize instance variables
        self.title = title
        self.lang = lang
        self.charset = charset
        self.stylesheets: list[str] = stylesheets

    @property
    def stylesheets(self) -> list[str]:
        """Gets the stylesheets."""
        return self._stylesheets

    @stylesheets.setter
    def stylesheets(self, value: list[str]) -> None:
        """Sets the stylesheets."""
        message = "stylesheets must be provided as a list of strings"
        if value is not None:
            if isinstance(value, list):
                if value and not all(isinstance(i, str) for i in value):
                    raise TypeError(message)
            else:
                raise TypeError(message)
        self._stylesheets: list[str] = value if value else []

    def add(self, *elements: Element) -> None:
        """Convenience wrapper for the self.elements.add method."""
        self.elements.add(*elements)

    def set(self, *elements: Element) -> None:
        """Convenience wrapper for the self.elements.set method."""
        self.elements.set(*elements)

    def insert(self, index: int, element: Element) -> None:
        """Convenience wrapper for the self.elements.insert method."""
        self.elements.insert(index, element)

    def update(self, index: int, element: Element) -> None:
        """Convenience wrapper for the self.elements.update method."""
        self.elements.update(index, element)

    def remove(self, index: int) -> None:
        """Convenience wrapper for the self.elements.remove method."""
        self.elements.remove(index)

    def pop(self, index: int = -1) -> Element:
        """Convenience wrapper for the self.elements.pop method."""
        return self.elements.pop(index)

    def clear(self) -> None:
        """Convenience wrapper for the self.elements.clear method."""
        self.elements.clear()

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
