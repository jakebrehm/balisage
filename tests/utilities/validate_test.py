"""
Contains tests for the utilities.validate module.
"""

import re

import pytest

from balisage.core import HTMLBuilder
from balisage.elements.styles import Div
from balisage.utilities.validate import (
    is_builder,
    is_element,
    is_valid_class_name,
    is_valid_type,
    raise_if_incorrect_type,
    sanitize_class_name,
    split_preserving_quotes,
)


def test_is_builder() -> None:
    """Tests the is_builder function."""

    # Override the abstract methods
    HTMLBuilder.__abstractmethods__ = set()

    # Test with with an HTMLBuilder object
    assert is_builder(HTMLBuilder()) is False

    # Test with a subclass of HTMLBuilder
    assert is_builder(Div()) is True

    # Test with other data types
    invalid_values = ["string", 1, 2.0, True, False, tuple(), dict(), None]
    for invalid_value in invalid_values:
        assert is_builder(invalid_value) is False


def test_is_element() -> None:
    """Tests the is_element function."""

    # Override the abstract methods
    HTMLBuilder.__abstractmethods__ = set()

    # Test with with an HTMLBuilder object
    assert is_element(HTMLBuilder()) is False

    # Test with a subclass of HTMLBuilder
    assert is_element(Div()) is True

    # Test with a string
    assert is_element("Test string") is True


def test_is_valid_type() -> None:
    """Tests the is_valid_type function."""

    # Test with valid types
    valid_types = [int, float, str, Div]
    assert is_valid_type(1, valid_types) is True
    assert is_valid_type(2.0, valid_types) is True
    assert is_valid_type("Test", valid_types) is True
    assert is_valid_type(Div(), valid_types) is True

    # Test with invalid types
    valid_types = [list, dict, tuple]
    invalid_types = [1, 2.0, "Test", Div(), True, False, None]
    for invalid_type in invalid_types:
        assert is_valid_type(invalid_type, valid_types) is False


def test_raise_if_incorrect_type() -> None:
    """Tests the raise_if_incorrect_type method of the Table class."""

    # Test with correct type
    raise_if_incorrect_type(1, expected_type=int)

    # Test with incorrect type
    message = "Expected int object, got str"
    with pytest.raises(TypeError, match=message):
        raise_if_incorrect_type("Test", expected_type=int)


def test_split_preserving_quotes() -> None:
    """Tests the split_preserving_quotes function."""

    # Test with only boolean attributes
    string = "required disabled itemscope"
    expected = ["required", "disabled", "itemscope"]
    assert split_preserving_quotes(string) == expected

    # Test with only non-boolean attributes
    string = "id='test' class='class1 class2' width='50'"
    expected = ["id='test'", "class='class1 class2'", "width='50'"]
    assert split_preserving_quotes(string) == expected

    # Test with boolean and non-boolean attributes
    string = "id='test' required disabled class='class1 class2' width='50' itemscope"
    expected = [
        "id='test'",
        "required",
        "disabled",
        "class='class1 class2'",
        "width='50'",
        "itemscope",
    ]
    assert split_preserving_quotes(string) == expected


def test_is_valid_class_name() -> None:
    """Tests the is_valid_class_name function."""

    # Test with valid class names
    valid_classes = [
        "class",  # Purely alphabetic, same case
        "Class",  # Purely alphabetic, mixed case
        "_class",  # Starts with an underscore
        "-class",  # Starts with a hyphen
        "-_class",  # Character following hyphen is underscore or letter
        "c",  # Too short
    ]
    for valid_class in valid_classes:
        assert is_valid_class_name(valid_class) is True

    # Test with invalid class names
    invalid_classes = [
        "1234567890",  # Purely numeric
        "$class",  # Starts with an invalid character
        "class!",  # Contains an invalid character
        "test class",  # Contains a space
        "--class",  # Character following hyphen is hyphen
        "-!class",  # Character following hyphen is invalid character
        "-",  # Starts with a hyphen but not 2 characters long
    ]
    for invalid_class in invalid_classes:
        assert is_valid_class_name(invalid_class) is False


def test_classes_sanitize_class_name() -> None:
    """Tests the sanitize_class_name function."""
    assert sanitize_class_name("class 1") == "class-1"
    assert sanitize_class_name("clAss2") == "class2"
    assert sanitize_class_name("Class 3") == "class-3"
    assert sanitize_class_name("  Class   4   ") == "class---4"
    # Test strip and lower options
    test_string = " ClASs 4  "
    assert sanitize_class_name(test_string, lower=False) == "ClASs-4"
    assert sanitize_class_name(test_string, strip=False) == "-class-4--"
    assert (
        sanitize_class_name(
            test_string,
            lower=False,
            strip=False,
        )
        == "-ClASs-4--"
    )
    # Test invalid class names
    message = r"Class name '123' (sanitized to '123') is invalid"
    with pytest.raises(ValueError, match=re.escape(message)):
        sanitize_class_name("123")
    message = r"Class name '-cl@Ss ' (sanitized to '-cl@ss') is invalid"
    with pytest.raises(ValueError, match=re.escape(message)):
        sanitize_class_name("-cl@Ss ")
