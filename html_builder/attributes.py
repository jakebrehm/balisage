"""
Contains code related to HTML attributes.
"""

from collections import OrderedDict
from typing import Self, TypeAlias

from .utilities import split_preserving_quotes


class Classes:
    """Class for managing classes for HTML elements."""

    DEFAULT_REPLACEMENTS: dict[str, str] = {" ": "-"}

    def __init__(
        self,
        *args: str,
    ) -> None:
        """Initializes the Classes object."""

        # Initialize instance variables
        self._classes = OrderedDict()
        self.reset_replacements()

        # Set the classes
        self.set(*args)

    @classmethod
    def from_string(cls, string: str) -> Self:
        """Creates a Classes object from a string."""
        return cls(*string.split(" "))

    @property
    def classes(self) -> OrderedDict[str:str]:
        """Gets the stored classes as an ordered dictionary.

        Keys are the original class names, values are the sanitized class names.
        """
        return self._classes

    @property
    def replacements(self) -> dict[str, str]:
        """Gets the replacements dictionary.

        The replacements dictionary controls the replacement of specifed
        characters in provided class names when they are sanitized.

        Keys are the characters to be replaced, values are the replacements.
        """
        return self._replacements

    @replacements.setter
    def replacements(self, replacements: dict[str, str]) -> None:
        """Sets the replacements dictionary."""
        self._replacements = replacements
        self.set(*self._classes.keys())

    def reset_replacements(self) -> None:
        """Resets the replacements dictionary to its default value."""
        self._replacements = self.DEFAULT_REPLACEMENTS

    def add(self, *args: str) -> None:
        """Adds classes to the list of classes."""

        # Determine the existing sanitized names
        old_sanitized_names = list(self._classes.values())
        # Determine the new sanitized names
        new_original_names = args
        new_sanitized_names = [self._sanitize_name(name) for name in args]
        new_names = zip(new_original_names, new_sanitized_names)
        # Check that duplicate classes aren't being added
        filtered_names = {
            new_original_name: new_sanitized_name
            for new_original_name, new_sanitized_name in new_names
            if new_sanitized_name not in old_sanitized_names
        }
        # Update the classes
        self._classes.update(filtered_names)

    def set(self, *args: str) -> None:
        """Sets the list of classes."""
        self._classes = {arg: self._sanitize_name(arg) for arg in args}

    def remove(self, name: str) -> tuple[str, str]:
        """Removes a class from the list of classes.

        Returns the removed class (if it exists) as a tuple, otherwise None.
        The tuple is in the form of (class name, sanitized class name).
        """

        # Try removing the class by its original name
        try:
            return name, self._classes.pop(name)
        except KeyError:
            pass
        # Try removing the class by its sanitized name
        for original_name, sanitized_name in self._classes.items():
            if sanitized_name == self._sanitize_name(name):
                return original_name, self._classes.pop(original_name)
        # If the class was not found, raise an exception
        raise KeyError(f"Class '{name}' not found.")

    def clear(self) -> None:
        """Clears the list of classes."""
        self._classes.clear()

    def _sanitize_name(
        self,
        name: str,
        lower: bool = True,
        strip: bool = True,
    ) -> str:
        """Converts a class string into a valid class name."""
        # TODO: Implement check for valid class names
        name = name.lower() if lower else name
        name = name.strip() if strip else name
        for k, v in self._replacements.items():
            name = name.replace(k, v)
        return name

    def construct(self) -> str:
        """Generates the class string."""
        return " ".join(self._classes.values())

    def __eq__(self, other: Self) -> bool:
        """Determines whether two Classes objects are equal."""
        return self._classes == other._classes

    def __str__(self) -> str:
        """Gets the string version of the object."""
        return self.construct()

    def __repr__(self) -> str:
        """Gets the string representation of the object."""
        arg_string = ", ".join(repr(c) for c in self._classes.keys())
        return f"{self.__class__.__name__}({arg_string})"


AttributeValue: TypeAlias = str | bool | None
AttributeDict: TypeAlias = dict[str, AttributeValue]
AttributeOrderedDict: TypeAlias = OrderedDict[str, AttributeValue]
AttributeMap: TypeAlias = AttributeOrderedDict | AttributeDict


class Attributes:
    """Class for managing attributes for HTML elements."""

    def __init__(self, attributes: AttributeMap | None = None) -> None:
        """Initializes the Attributes object."""

        # Initialize instance variables
        self._attributes: AttributeOrderedDict = OrderedDict()

        # Set the classes
        if attributes is not None:
            self.set(attributes)

    @classmethod
    def from_string(cls, string: str) -> Self:
        """Creates an Attributes object from a string."""
        attributes = OrderedDict()
        pairs = split_preserving_quotes(string)
        for pair in pairs:
            key, _, value = pair.partition("=")
            value = value.strip("'")
            if not value:
                value = True
            attributes[key] = value
        return cls(attributes)

    @property
    def attributes(self) -> AttributeOrderedDict:
        """Gets the stored attributes.

        Keys are the attribute names, values are the attribute values.
        """
        return self._attributes

    def add(self, attributes: AttributeMap) -> None:
        """Adds attributes to the list of attributes."""
        if "class" in attributes and isinstance(attributes["class"], str):
            attributes["class"] = Classes.from_string(attributes["class"])
        self._attributes.update(attributes)

    def set(self, attributes: AttributeMap) -> None:
        """Sets the list of attributes."""
        if "class" in attributes and isinstance(attributes["class"], str):
            attributes["class"] = Classes.from_string(attributes["class"])
        self._attributes = OrderedDict(attributes)

    def remove(self, name: str) -> AttributeValue | None:
        """Removes attributes from the list of attributes.

        Returns the removed attribute (if it exists) as a tuple, otherwise None.
        The tuple is in the form of (attribute name, attribute value).
        """
        return name, self._attributes.pop(name)

    def clear(self) -> None:
        """Clears the attributes of the HTML object."""
        self._attributes.clear()

    def construct(self) -> str:
        """Generates the attribute string."""
        pairs = []
        for key, value in self._attributes.items():
            # None and True values are boolean attributes, False will be ignored
            if (value is None) or (isinstance(value, bool) and value):
                pairs.append(f"{key}")
            elif value:
                pairs.append(f"{key}='{value}'")
        return " ".join(pairs)

    def __getitem__(self, key: str) -> AttributeValue:
        """Gets an attribute from the Attributes object."""
        return self._attributes[key]

    def __setitem__(self, key: str, value: AttributeValue) -> None:
        """Sets an attribute in the Attributes object."""
        self._attributes[key] = value

    def __eq__(self, other: Self) -> bool:
        """Determines whether two Attributes objects are equal."""
        return self._attributes == other._attributes

    def __str__(self) -> str:
        """Gets the string version of the object."""
        return self.construct()

    def __repr__(self) -> str:
        """Gets the string representation of the object."""
        return f"{self.__class__.__name__}(attributes={self._attributes!r})"


ClassesType: TypeAlias = Classes | str | list[str]
AttributesType: TypeAlias = Attributes | AttributeMap
