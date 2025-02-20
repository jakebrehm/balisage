"""
Contains tests for the core module.
"""

import pytest

from html_builder.attributes import Attributes, Classes
from html_builder.core import HTMLBuilder


@pytest.fixture()
def builder() -> HTMLBuilder:
    """Creates a sample HTMLBuilder object with some attributes."""
    attributes = {"id": "test", "disabled": True}
    return HTMLBuilder(attributes=Attributes(attributes))


def test_html_builder_init() -> None:
    """Tests the initialization of the HTMLBuilder class."""

    # Override the abstract methods
    HTMLBuilder.__abstractmethods__ = set()

    # Pass nothing
    builder = HTMLBuilder()
    assert builder.attributes == Attributes()
    assert builder.classes is None

    # Pass attributes
    builder = HTMLBuilder(attributes=Attributes({"id": "test"}))
    assert builder.attributes == Attributes({"id": "test"})
    assert builder.classes is None

    # Pass classes via attributes argument
    expected_classes = Classes("class 1", "class2")
    expected_attributes = Attributes({"class": "class-1 class2"})
    builder = HTMLBuilder(attributes=expected_attributes)
    assert builder.attributes == expected_attributes
    assert builder.attributes.classes == expected_classes
    assert builder.classes == expected_classes

    # Pass classes via classes argument (not overriding attributes)
    builder = HTMLBuilder(classes=expected_classes)
    assert builder.attributes == expected_attributes
    assert builder.attributes.classes == expected_classes
    assert builder.classes == expected_classes

    # Pass classes via classes argument (overriding attributes)
    passed_attributes = Attributes({"id": "test", "class": "class3 Class-4"})
    expected_attributes = Attributes({"id": "test", "class": "class-1 class2"})
    expected_classes = Classes("class 1", "class2")  # TODO: Remove
    builder = HTMLBuilder(attributes=passed_attributes, classes=expected_classes)
    assert builder.attributes == expected_attributes
    assert builder.attributes.classes == expected_classes
    assert builder.classes == expected_classes


def test_html_builder_repr(builder: HTMLBuilder) -> None:
    """Tests the __repr__ method of the HTMLBuilder class."""
    expected = (
        "HTMLBuilder(attributes="
        "Attributes(attributes="
        "{'id': 'test', 'disabled': True}"
        "))"
    )
    assert repr(builder) == expected
