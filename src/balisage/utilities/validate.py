"""
Contains validation-related code for the package.
"""

import re
from typing import Any

# MARK: Types


def is_builder(object: Any) -> bool:
    """Determines whether an object is a subclass of HTMLBuilder."""
    from ..types import Builder

    return issubclass(type(object), Builder)


def is_element(object: Any) -> bool:
    """Determines whether an object is a valid Element."""
    return is_builder(object) or isinstance(object, str)


# MARK: Classes


def is_valid_class_name(name: str) -> bool:
    """Determines whether a string is a valid HTML/CSS class name."""
    return re.match(r"^-?[_a-zA-Z]+[_a-zA-Z0-9-]*$", name) is not None


# TODO: Move class name sanitization function here


# MARK: Attributes


def split_preserving_quotes(string: str) -> list[str]:
    """Splits an attribute string into a list of strings, preserving quotes."""
    return re.findall(r"[^'\s]+='[^']*'|\S+", string)


# TODO: Move attribute string partitioning function here
