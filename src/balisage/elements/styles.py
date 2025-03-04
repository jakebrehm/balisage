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


class Bold(Span):
    """Constructs an HTML bold element."""

    def __init__(
        self,
        elements: ElementsType | str | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Bold object."""

        # Initialize the builder
        super().__init__(
            elements=elements,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "b"


class Strong(Span):
    """Constructs an HTML strong element."""

    def __init__(
        self,
        elements: ElementsType | str | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Strong object."""

        # Initialize the builder
        super().__init__(
            elements=elements,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "strong"


class Italics(Span):
    """Constructs an HTML italics element."""

    def __init__(
        self,
        elements: ElementsType | str | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Italics object."""

        # Initialize the builder
        super().__init__(
            elements=elements,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "i"


class Emphasis(Span):
    """Constructs an HTML emphasis element."""

    def __init__(
        self,
        elements: ElementsType | str | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Emphasis object."""

        # Initialize the builder
        super().__init__(
            elements=elements,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "em"


class Underline(Span):
    """Constructs an HTML underline element."""

    def __init__(
        self,
        elements: ElementsType | str | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Underline object."""

        # Initialize the builder
        super().__init__(
            elements=elements,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "u"


class Strikethrough(Span):
    """Constructs an HTML strikethrough element."""

    def __init__(
        self,
        elements: ElementsType | str | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Strikethrough object."""

        # Initialize the builder
        super().__init__(
            elements=elements,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "s"


class Subscript(Span):
    """Constructs an HTML subscript element."""

    def __init__(
        self,
        elements: ElementsType | str | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Subscript object."""

        # Initialize the builder
        super().__init__(
            elements=elements,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "sub"


class Superscript(Span):
    """Constructs an HTML superscript element."""

    def __init__(
        self,
        elements: ElementsType | str | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Superscript object."""

        # Initialize the builder
        super().__init__(
            elements=elements,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "sup"
