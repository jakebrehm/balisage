"""
Contains code for all list-related HTML elements.
"""

from ..core import GenericElement
from ..types import AttributesType, ClassesType, Element, ElementsType


class ListItem(GenericElement):
    """Constructs an HTML list item element."""

    def __init__(
        self,
        elements: ElementsType | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the ListItem object."""

        # Initialize the builder
        super().__init__(
            tag="li",
            elements=elements,
            attributes=attributes,
            classes=classes,
        )


class OrderedList(GenericElement):
    """Constructs an HTML ordered list."""

    def __init__(
        self,
        elements: list[ListItem] | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the OrderedList object."""

        # Initialize the builder
        super().__init__(
            tag="ol",
            elements=None,
            attributes=attributes,
            classes=classes,
        )

        self.elements.valid_types = ListItem

        # Set the elements
        if elements is not None:
            self.set(*elements)

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


class UnorderedList(OrderedList):
    """Constructs an HTML unordered list."""

    def __init__(
        self,
        elements: list[ListItem] | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the UnorderedList object."""

        # Initialize the builder
        super().__init__(
            elements=elements,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "ul"
