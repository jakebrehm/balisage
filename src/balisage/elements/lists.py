"""
Contains code for all list-related HTML elements.
"""

from ..core import GenericElement
from ..types import AttributesType, ClassesType, Element, ElementsType
from ..utilities.validate import raise_if_incorrect_type


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

        # Validate the types of the elements
        if elements and not all(isinstance(e, ListItem) for e in elements):
            raise TypeError(  # TODO: Move functionality to Elements
                f"All elements of {self.__class__.__name__} must be of type "
                f"{ListItem.__name__}"
            )

        # Initialize the builder
        super().__init__(
            tag="ol",
            elements=elements,
            attributes=attributes,
            classes=classes,
        )

    def add(self, *elements: Element) -> None:
        """Convenience wrapper for the self.elements.add method."""
        for element in elements:  # TODO: Move functionality to Elements
            raise_if_incorrect_type(element, expected_type=ListItem)
        self.elements.add(*elements)

    def set(self, *elements: Element) -> None:
        """Convenience wrapper for the self.elements.set method."""
        for element in elements:
            raise_if_incorrect_type(element, expected_type=ListItem)
        self.elements.set(*elements)

    def insert(self, index: int, element: Element) -> None:
        """Convenience wrapper for the self.elements.insert method."""
        raise_if_incorrect_type(element, expected_type=ListItem)
        self.elements.insert(index, element)

    def update(self, index: int, element: Element) -> None:
        """Convenience wrapper for the self.elements.update method."""
        raise_if_incorrect_type(element, expected_type=ListItem)
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
