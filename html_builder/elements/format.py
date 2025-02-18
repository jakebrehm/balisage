"""
Contains code for all formatting-related HTML elements.
"""

from typing import Any

from ..core import HTMLBuilder


class LineBreak(HTMLBuilder):
    """Constructs an HTML line break."""

    def __init__(self, **kwargs) -> None:
        """Initializes the LineBreak object."""

        # Initialize the builder
        super().__init__(classes=None, **kwargs)
        self.tag = "br"

    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        return f"<{self.tag}>"


class HorizontalRule(HTMLBuilder):
    """Constructs an HTML horizontal rule."""

    def __init__(
        self,
        classes: str | list[str] | None = None,
        **kwargs,
    ) -> None:
        """Initializes the HorizontalRule object."""

        # Initialize the builder
        super().__init__(classes=classes, **kwargs)
        self.tag = "hr"

    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        return f"<{self.tag}{self.attributes_to_string()}>"


class Div(HTMLBuilder):
    """Constructs an HTML div."""

    def __init__(
        self,
        data: Any | list[Any] | None = None,
        classes: str | list[str] | None = None,
        **kwargs,
    ) -> None:
        """Initializes the Div object."""

        # Initialize the builder
        super().__init__(classes, **kwargs)
        self.tag = "div"

        # Set the data
        if data is not None:
            self.set_data(data)

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

    def add(self, data: Any) -> None:
        """Adds data. Simple wrapper around add_data."""
        self.add_data(data)

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
