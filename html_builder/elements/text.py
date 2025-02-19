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


class Paragraph(Text):
    """Constructs an HTML paragraph."""

    def __init__(
        self,
        text: str,
        classes: str | list[str] | None = None,
        **kwargs,
    ) -> None:
        """Initializes the Paragraph object."""

        # Initialize the builder
        super().__init__(text, TextType.P, classes, **kwargs)


class Heading1(Text):
    """Constructs an HTML heading (size 1)."""

    def __init__(
        self,
        text: str,
        classes: str | list[str] | None = None,
        **kwargs,
    ) -> None:
        """Initializes the Heading1 object."""

        # Initialize the builder
        super().__init__(text, TextType.H1, classes, **kwargs)


class Heading2(Text):
    """Constructs an HTML heading (size 2)."""

    def __init__(
        self,
        text: str,
        classes: str | list[str] | None = None,
        **kwargs,
    ) -> None:
        """Initializes the Heading2 object."""

        # Initialize the builder
        super().__init__(text, TextType.H2, classes, **kwargs)


class Heading3(Text):
    """Constructs an HTML heading (size 3)."""

    def __init__(
        self,
        text: str,
        classes: str | list[str] | None = None,
        **kwargs,
    ) -> None:
        """Initializes the Heading3 object."""

        # Initialize the builder
        super().__init__(text, TextType.H3, classes, **kwargs)


class Heading4(Text):
    """Constructs an HTML heading (size 4)."""

    def __init__(
        self,
        text: str,
        classes: str | list[str] | None = None,
        **kwargs,
    ) -> None:
        """Initializes the Heading4 object."""

        # Initialize the builder
        super().__init__(text, TextType.H4, classes, **kwargs)


class Heading5(Text):
    """Constructs an HTML heading (size 5)."""

    def __init__(
        self,
        text: str,
        classes: str | list[str] | None = None,
        **kwargs,
    ) -> None:
        """Initializes the Heading5 object."""

        # Initialize the builder
        super().__init__(text, TextType.H5, classes, **kwargs)


class Heading6(Text):
    """Constructs an HTML heading (size 6)."""

    def __init__(
        self,
        text: str,
        classes: str | list[str] | None = None,
        **kwargs,
    ) -> None:
        """Initializes the Heading6 object."""

        # Initialize the builder
        super().__init__(text, TextType.H6, classes, **kwargs)
