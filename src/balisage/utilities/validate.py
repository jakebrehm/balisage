"""
Contains validation-related code for the package.
"""

import re
from typing import Any, Type

# MARK: Types and conversions


def is_builder(object: Any) -> bool:
    """Determines whether an object is a subclass of HTMLBuilder."""
    from ..types import Builder

    return issubclass(type(object), Builder) and type(object) is not Builder


def is_element(object: Any) -> bool:
    """Determines whether an object is a valid Element."""
    return is_builder(object) or isinstance(object, str)


def types_to_tuple(value: Any) -> tuple[Any, ...]:
    """Converts a value for expected types to a tuple if necessary."""
    if isinstance(value, tuple):
        return value
    elif isinstance(value, list):
        return tuple(value)
    elif not isinstance(value, Type):
        instance_type = type(value).__name__
        raise TypeError(f"Expected a type, got instance of {instance_type}")
    return (value,)


def is_valid_type(
    value: Any,
    expected_types: Type | list[Type] | tuple[Type, ...],
) -> bool:
    """Determines whether the input is of the expected type."""
    return isinstance(value, types_to_tuple(expected_types))


def raise_for_type(
    value: Any,
    expected_types: Type | list[Type] | tuple[Type, ...],
) -> None:
    """Determines whether the input is of the expected type."""
    expected_types = types_to_tuple(expected_types)
    if not is_valid_type(value, expected_types):
        type_names = [t.__name__ for t in expected_types]
        type_names = (
            f"({', '.join(type_names)}{',' if len(type_names) == 1 else ''})"
        )
        raise TypeError(
            f"Got {type(value).__name__}, expected one of {type_names}"
        )


# MARK: Classes


def is_valid_class_name(name: str) -> bool:
    """Determines whether a string is a valid HTML/CSS class name."""
    return re.match(r"^-?[_a-zA-Z]+[_a-zA-Z0-9-]*$", name) is not None


def sanitize_class_name(
    name: str,
    lower: bool = True,
    strip: bool = True,
    replacements: dict[str, str] | None = None,
) -> str:
    """Converts a class string into a valid class name."""
    if replacements is None:
        replacements = {" ": "-"}
    original_name = name
    name = name.lower() if lower else name
    name = name.strip() if strip else name
    for k, v in replacements.items():
        name = name.replace(k, v)
    if not is_valid_class_name(name):
        raise ValueError(
            f"Class name '{original_name}' (sanitized to '{name}') is invalid"
        )
    return name


# MARK: Attributes


def split_preserving_quotes(string: str) -> list[str]:
    """Splits an attribute string into a list of strings, preserving quotes."""
    return re.findall(r"[^'\s]+='[^']*'|\S+", string)
