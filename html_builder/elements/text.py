"""
Contains code for all text-related HTML elements.
"""

from enum import Enum
from typing import Any

from ..core import HTMLBuilder


class TextType(Enum):
    P = "p"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"


class Text(HTMLBuilder):
    """Constructs HTML text."""

    def __init__(
        self,
        text: str,
        tag: TextType = TextType.P,
        classes: str | list[str] | None = None,
        **kwargs,
    ) -> None:
        """Initializes the Text object."""

        # Initialize the builder
        super().__init__(classes, **kwargs)
        self.tag = tag.value

        # Set the text
        self.set_text(text)

    def set_text(self, text: Any) -> None:
        """Sets the text."""
        self.clear_elements()
        self.add_element(text)

    def construct(self) -> str:
        """Generates HTML from the stored elements."""

        # Open the tag
        html = f"<{self.tag}{self.attributes_to_string()}>"

        # Add the data
        for element in self.elements:
            html += f"{element}"

        # Close the tag and return the HTML
        html += f"</{self.tag}>"
        return html
