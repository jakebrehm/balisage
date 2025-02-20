"""
Contains core functionality for the package.
"""

from abc import ABC, abstractmethod
from typing import Any

from .attributes import Attributes, AttributesType, Classes, ClassesType


class HTMLBuilder(ABC):
    """Base class for HTML Builder objects."""

    def __init__(
        self,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the HTMLTable object."""

        # Initialize instance variables
        self._elements: list[Any] = []
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

    def add_element(self, element: Any) -> None:
        """Adds an element to the HTML object."""
        self._elements.append(element)

    def add_elements(self, elements: list[Any]) -> None:
        """Adds elements to the HTML object."""
        self._elements.extend(elements)

    def insert_element(self, index: int, element: Any) -> None:
        """Inserts an element at the specified index."""
        self._elements.insert(index, element)

    def update_element(self, index: int, element: Any) -> None:
        """Updates the element at the specified index."""
        self._elements[index] = element

    def remove_element(self, index: int) -> Any:
        """Removes and returns the element at the specified index."""
        return self._elements.pop(index)

    def clear_elements(self) -> None:
        """Clears the classes of the HTML object."""
        self._elements.clear()

    # def set_attribute( # TODO: Remove block
    #     self,
    #     attribute: str | dict[str:Any],
    #     value: Any | None = None,
    # ) -> None:
    #     """Set an attributes of the HTML object."""

    #     # Check if the first input is a dictionary or an attribute name
    #     if isinstance(attribute, dict) and value is None:
    #         self.update_attributes(attribute)
    #     elif isinstance(attribute, str) and value is not None:
    #         self.update_attributes({attribute: value})
    #     else:
    #         raise TypeError(
    #             f"{self.set_attribute.__name__} accepts either a single "
    #             "dictionary argument, or a string and its corresponding "
    #             "value as two arguments."
    #         )

    # def set_attributes(self, attributes: dict[str : Any | None]) -> None:
    #     """Sets attributes of the HTML object."""
    #     self.update_attributes(attributes)

    # def update_attributes(self, attributes: dict[str : Any | None]) -> None:
    #     """Updates attributes of the HTML object."""
    #     self._attributes.update(attributes)

    # def pop_attribute(self, attribute: str) -> Any | None:
    #     """Removes an attribute from the HTML object and returns it."""
    #     return self._attributes.pop(attribute)

    # def clear_attributes(self) -> None:
    #     """Clears the attributes of the HTML object."""
    #     self._attributes.clear()

    # def add_class(self, name: str) -> None:
    #     """Adds a class to the HTML object."""
    #     if "class" not in self._attributes:
    #         self._attributes["class"] = []
    #     self._attributes["class"].add(name)

    # def remove_class(self, name: str) -> None:
    #     """Removes a class from the HTML object."""
    #     if "class" in self._attributes:
    #         self._attributes["class"].remove(name)

    # def set_classes(self, names: ClassesType) -> None:
    #     """Adds a class to the HTML object."""

    #     # If the names are already a Classes object, return
    #     if isinstance(names, Classes):
    #         self._attributes["class"] = names
    #         return

    #     # Convert the class name to a list if necessary
    #     if isinstance(names, str):
    #         names = [names]

    #     # Verify that the list only contains strings
    #     is_not_list = not isinstance(names, list)
    #     is_not_all_strings = any(not isinstance(n, str) for n in names)
    #     if is_not_list or is_not_all_strings:
    #         raise TypeError(
    #             f"{self.set_classes.__name__} only accepts a string or a "
    #             "list of strings."
    #         )

    #     # Clear the stored classes and add the provided ones
    #     self._attributes["class"] = Classes(*names)

    # def clear_classes(self) -> list[str] | None:
    #     """Clears the classes of the HTML object.

    #     Returns the deleted classes.
    #     """
    #     return self._attributes.pop("class", None)

    # def attributes_to_string(self) -> str:
    #     """Builds an attribute string from a dictionary of attributes."""
    #     return " " + str(self._attributes)
    #     # result = []
    #     # for key, value in self._attributes.attributes.items():
    #     #     if (value is None) or (isinstance(value, bool) and value):
    #     #         string = f"{key}"
    #     #     elif value:
    #     #         string = f"{key}='{value}'"
    #     #     else:
    #     #         continue
    #     #     result.append(string)
    #     # return (" " + " ".join(result)) if result else ""

    def __str__(self) -> str:
        """Gets a string version of the object."""
        return self.construct()

    def __repr__(self) -> str:
        """Gets a string representation of the object."""
        return f"{self.__class__.__name__}(attributes={self._attributes!r})"
