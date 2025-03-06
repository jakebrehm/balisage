"""
Contains code for all link-related HTML elements.
"""

from ..core import GenericElement
from ..types import AttributesType, ClassesType, ElementsType


class Link(GenericElement):
    """Constructs an HTML link element."""

    def __init__(
        self,
        elements: ElementsType | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Link object."""

        # Initialize the builder
        super().__init__(
            tag="a",
            elements=elements,
            attributes=attributes,
            classes=classes,
        )
