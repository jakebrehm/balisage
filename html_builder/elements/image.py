"""
Contains code for all formatting-related HTML elements.
"""

from ..core import HTMLBuilder


class Image(HTMLBuilder):
    """Constructs an HTML image."""

    def __init__(
        self,
        classes: str | list[str] | None = None,
        **kwargs,
    ) -> None:
        """Initializes the Image object."""

        # Initialize the builder
        super().__init__(classes=classes, **kwargs)
        self.tag = "img"

    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        return f"<{self.tag}{self.attributes_to_string()}>"
