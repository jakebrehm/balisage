"""
Contains code for all style-related HTML elements.
"""

from typing import Any

from ..attributes import Elements
from ..core import GenericElement
from ..types import AttributesType, ClassesType, ElementsType


class Div(GenericElement):
    """Constructs an HTML div."""

    def __init__(
        self,
        elements: ElementsType | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Div object."""

        # Initialize the builder
        super().__init__(
            tag="div",
            elements=elements,
            attributes=attributes,
            classes=classes,
        )


class Span(GenericElement):
    """Constructs an HTML span."""

    def __init__(
        self,
        elements: ElementsType | str | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Span object."""

        # Convert a string into an Elements object
        if isinstance(elements, str):
            elements = Elements(elements)

        # Initialize the builder
        super().__init__(
            tag="span",
            elements=elements,
            attributes=attributes,
            classes=classes,
        )

    def __add__(self, other: Any) -> str:
        """Overloads the addition operator when the instance is on the left."""
        if isinstance(other, str):
            return self.construct() + other
        raise TypeError(
            f"Invalid type {type(other).__name__} for addition on "
            f"{self.__class__.__name__}; must be {str.__name__}"
        )

    def __radd__(self, other: Any) -> str:
        """Overloads the addition operator when the instance is on the right."""
        if isinstance(other, str):
            return other + self.construct()
        raise TypeError(
            f"Invalid type {type(other).__name__} for reverse addition on "
            f"{self.__class__.__name__}; must be {str.__name__}"
        )
