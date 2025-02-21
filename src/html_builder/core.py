"""
Contains core functionality for the package.
"""

from abc import ABC, abstractmethod
from typing import Any

from .attributes import (
    Attributes,
    AttributesType,
    Classes,
    ClassesType,
    Elements,
    ElementsType,
)


class HTMLBuilder(ABC):
    """Base class for HTML Builder objects."""

    def __init__(
        self,
        elements: ElementsType | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the HTMLTable object."""

        # Initialize instance variables
        self._elements = elements if elements else Elements()
        self._attributes = attributes if attributes else Attributes()

        # Set the classes if any were provided
        if classes is not None:
            self._attributes.classes = classes

    @abstractmethod
    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        pass

    def save(self, filepath: str) -> None:
        """Saves the HTML data to the specified filepath."""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.construct())

    @property
    def elements(self) -> list[Any]:
        """Gets the stored elements."""
        return self._elements

    @property
    def attributes(self) -> Attributes:
        """Gets the stored attributes."""
        return self._attributes

    @property
    def classes(self) -> Classes | None:
        """Gets the stored classes."""
        return self._attributes.classes

    def __str__(self) -> str:
        """Gets a string version of the object."""
        return self.construct()

    def __repr__(self) -> str:
        """Gets a string representation of the object."""
        return f"{self.__class__.__name__}(attributes={self._attributes!r})"
