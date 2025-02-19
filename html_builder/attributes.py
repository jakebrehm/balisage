"""
Contains code related to HTML attributes.
"""

from collections import OrderedDict
from typing import Self


class Classes:
    """Class for managing classes for HTML elements."""

    def __init__(
        self,
        *args: list[str],
    ) -> None:
        """Initializes the Classes object."""

        # Initialize replacement lookup
        self._replacements = {
            " ": "-",
        }

        # Initialize instance variables
        self._classes = OrderedDict()

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

    def add(self, name: str) -> None:
        """Adds a class to the list of classes."""
        self._classes[name] = self._sanitize_name(name)

    def set(self, *args: list[str]) -> None:
        """Sets the list of classes."""
        self._classes = {arg: self._sanitize_name(arg) for arg in args}

    def remove(self, name: str) -> tuple[str, str] | None:
        """Removes a class from the list of classes.

        Returns the removed class (if it exists) as a tuple, otherwise None.
        The tuple is in the form of (class name, sanitized class name).
        """
        try:
            return (name, self._classes.pop(name))
        except KeyError:
            pass
        try:
            sanitized_name = self._sanitize_name(name)
            return (sanitized_name, self._classes.pop(sanitized_name))
        except KeyError:
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
        name = name.lower() if lower else name
        name = name.strip() if strip else name
        for k, v in self._replacements.items():
            name = name.replace(k, v)
        return name

    def construct(self) -> str:
        """Generates the class string."""
        return " ".join(self._classes.values())

    def __str__(self) -> str:
        """Gets the string version of the object."""
        string = self.construct()
        return f"class='{string}'" if string else ""

    def __repr__(self) -> str:
        """Gets the string representation of the object."""
        arg_string = ", ".join(repr(c) for c in self._classes.keys())
        return f"{self.__class__.__name__}({arg_string})"
