"""
Contains code for all formatting-related HTML elements.
"""

from typing import Any

from ..attributes import AttributesType, ClassesType
from ..core import HTMLBuilder


class LineBreak(HTMLBuilder):
    """Constructs an HTML line break."""

    def __init__(
        self,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the LineBreak object."""

        # Initialize the builder
        super().__init__(attributes=attributes, classes=classes)
        self.tag = "br"

    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        attributes_string = f" {self.attributes}" if self.attributes else ""
        return f"<{self.tag}{attributes_string}>"


class HorizontalRule(LineBreak):
    """Constructs an HTML horizontal rule."""

    def __init__(
        self,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the HorizontalRule object."""

        # Initialize the builder
        super().__init__(attributes=attributes, classes=classes)
        self.tag = "hr"


class Div(HTMLBuilder):
    """Constructs an HTML div."""

    def __init__(
        self,
        data: Any | list[Any] | None = None,  # TODO: Rework to use Elements
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Div object."""

        # Initialize the builder
        super().__init__(attributes=attributes, classes=classes)
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
        attributes_string = f" {self.attributes}" if self.attributes else ""
        html = f"<{self.tag}{attributes_string}>"

        # Add the data
        for element in self.elements:
            html += f"{element}"

        # Close the tag and return the HTML
        html += f"</{self.tag}>"
        return html
