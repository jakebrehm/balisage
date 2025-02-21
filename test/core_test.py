"""
Contains tests for the core module.
"""

import pytest

from html_builder import Div, LineBreak
from html_builder.attributes import Attributes, Classes, Elements
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
    assert builder.elements == Elements()

    # Pass attributes
    builder = HTMLBuilder(attributes=Attributes({"id": "test"}))
    assert builder.attributes == Attributes({"id": "test"})
    assert builder.classes is None
    assert builder.elements == Elements()

    # Pass classes via attributes argument
    expected_classes = Classes("class 1", "class2")
    expected_attributes = Attributes({"class": "class-1 class2"})
    builder = HTMLBuilder(attributes=expected_attributes)
    assert builder.attributes == expected_attributes
    assert builder.attributes.classes == expected_classes
    assert builder.classes == expected_classes
    assert builder.elements == Elements()

    # Pass classes via classes argument (not overriding attributes)
    builder = HTMLBuilder(classes=expected_classes)
    assert builder.attributes == expected_attributes
    assert builder.attributes.classes == expected_classes
    assert builder.classes == expected_classes
    assert builder.elements == Elements()

    # Pass classes via classes argument (overriding attributes)
    passed_attributes = Attributes({"id": "test", "class": "class3 Class-4"})
    expected_attributes = Attributes({"id": "test", "class": "class-1 class2"})
    builder = HTMLBuilder(attributes=passed_attributes, classes=expected_classes)
    assert builder.attributes == expected_attributes
    assert builder.attributes.classes == expected_classes
    assert builder.classes == expected_classes
    assert builder.elements == Elements()

    # Pass elements as an Elements object
    expected_elements = Elements(Div(), LineBreak())
    builder = HTMLBuilder(elements=expected_elements)
    assert builder.attributes == Attributes()
    assert builder.classes is None
    assert builder.elements == expected_elements

    # Pass elements as a list of elements
    passed_elements = [Div(), LineBreak()]
    expected_elements = Elements(*passed_elements)
    builder = HTMLBuilder(elements=passed_elements)
    assert builder.attributes == Attributes()
    assert builder.classes is None
    assert builder.elements == expected_elements


def test_html_builder_repr(builder: HTMLBuilder) -> None:
    """Tests the __repr__ method of the HTMLBuilder class."""
    expected = (
        "HTMLBuilder(attributes="
        "Attributes(attributes="
        "{'id': 'test', 'disabled': True}"
        "))"
    )
    assert repr(builder) == expected
