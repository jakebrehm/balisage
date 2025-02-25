"""
Contains tests for the core module.
"""

import os
import pathlib
from copy import deepcopy

import pytest

from html_builder import Div, LineBreak
from html_builder.attributes import Attributes, Classes, Elements
from html_builder.core import HTMLBuilder
from html_builder.elements.basic import Page
from html_builder.elements.format import HorizontalRule
from html_builder.elements.text import Heading1, Paragraph

# Determine if beautifulsoup4 is installed
try:
    import bs4  # noqa: F401

    BS4_INSTALLED = True
except ImportError:
    BS4_INSTALLED = False

# MARK: Fixtures


@pytest.fixture()
def builder() -> HTMLBuilder:
    """Creates a sample HTMLBuilder object with some attributes."""
    attributes = {"id": "test", "disabled": True}
    return HTMLBuilder(
        elements=Elements(LineBreak(), HorizontalRule()),
        attributes=Attributes(attributes),
    )


# MARK: HTMLBuilder


def test_html_builder_init() -> None:
    """Tests the initialization of the HTMLBuilder class."""

    # Override the abstract methods
    HTMLBuilder.__abstractmethods__ = set()

    # Pass nothing
    builder = HTMLBuilder()
    assert builder.attributes == Attributes()
    assert builder.classes == Classes()
    assert builder.elements == Elements()

    # Pass attributes
    builder = HTMLBuilder(attributes=Attributes({"id": "test"}))
    assert builder.attributes == Attributes({"id": "test"})
    assert builder.classes == Classes()
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
    assert builder.classes == Classes()
    assert builder.elements == expected_elements

    # Pass elements as a list of elements
    passed_elements = [Div(), LineBreak()]
    expected_elements = Elements(*passed_elements)
    builder = HTMLBuilder(elements=passed_elements)
    assert builder.attributes == Attributes()
    assert builder.classes == Classes()
    assert builder.elements == expected_elements


def test_html_builder_prettify() -> None:
    """Tests the prettify method of the HTMLBuilder class."""

    # Create a test page
    page = Page(
        elements=Elements(
            Heading1("Test heading"),
            HorizontalRule(),
            Div(
                elements=Elements(
                    Paragraph("Test paragraph 1"),
                    LineBreak(),
                    Paragraph("Test paragraph 2"),
                )
            ),
        ),
        title="Test title",
    )

    # Determine the current directory
    current_directory = pathlib.Path(__file__).parent.resolve()

    # Test with default arguments
    if BS4_INSTALLED:
        filepath = os.path.join(current_directory, r"_data/prettify_indent_2.html")
        with open(filepath, "r", encoding="utf-8") as f:
            expected = f.read()
        assert page.prettify() == expected

        # Test with a different indent
        filepath = os.path.join(current_directory, r"_data/prettify_indent_4.html")
        with open(filepath, "r", encoding="utf-8") as f:
            expected = f.read()
        assert page.prettify(indent=4) == expected

    else:
        filepath = os.path.join(current_directory, r"_data/prettify_indent_0.html")
        with open(filepath, "r", encoding="utf-8") as f:
            expected = f.read()
        assert page.construct() == expected


def test_html_builder_save() -> None:
    """Tests the save method of the HTMLBuilder class."""

    # Override the abstract construct method
    old_method = HTMLBuilder.construct
    HTMLBuilder.construct = lambda _: (
        "<!DOCTYPE html><html><body><p>Test paragraph</p></body></html>"
    )
    builder = HTMLBuilder()

    # Determine the filepath to save to and create any necessary directories
    current_directory = pathlib.Path(__file__).parent.resolve()
    filepath = os.path.join(current_directory, r"_temp/test.html")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    builder.save(filepath)
    assert os.path.exists(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        expected = f.read()
    assert expected == builder.construct()
    os.remove(filepath)

    # Test with prettify
    filepath = os.path.join(current_directory, r"_temp/prettify_save.html")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    builder.save(filepath, prettify=True)
    assert os.path.exists(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        expected = f.read()
    if BS4_INSTALLED:
        assert expected == builder.prettify()
    else:
        assert expected == builder.construct()

    os.remove(filepath)

    # Reset the method
    HTMLBuilder.construct = old_method


def test_html_builder_eq(builder: HTMLBuilder) -> None:
    """Tests the __eq__ method of the HTMLBuilder class."""

    # Compare to itself
    assert builder == builder

    # Compare to object with the same elements and attributes
    expected_attributes = Attributes({"id": "test", "disabled": True})
    expected_elements = Elements(LineBreak(), HorizontalRule())
    expected_builder = HTMLBuilder(
        elements=expected_elements,
        attributes=expected_attributes,
    )
    assert builder == expected_builder

    # Compare to itself with attributes changed
    expected_builder = deepcopy(builder)
    expected_builder.attributes.add({"required": False})
    assert builder != expected_builder

    # Compare to object with different attributes
    expected_attributes = Attributes({"id": "test-1"})
    expected_builder = HTMLBuilder(
        elements=expected_elements,
        attributes=expected_attributes,
    )
    assert builder != expected_builder

    # Compare to itself with elements changed
    expected_builder = deepcopy(builder)
    expected_builder.elements.add(LineBreak())
    assert builder != expected_builder

    # Compare to object with different elements
    expected_elements = Elements(Div(), HorizontalRule())
    expected_builder = HTMLBuilder(
        elements=expected_elements,
        attributes=expected_attributes,
    )
    assert builder != expected_builder

    # Compare to object with different elements and attributes
    expected_attributes = Attributes({"id": "test-1"})
    expected_elements = Elements(Div(), HorizontalRule())
    expected_builder = HTMLBuilder(
        elements=expected_elements,
        attributes=expected_attributes,
    )
    assert builder != expected_builder

    # Compare to other data types
    assert builder != 1
    assert builder != 2.0
    assert builder is not True
    assert builder is not False
    assert builder != tuple()
    assert builder != list()
    assert builder != dict()
    assert builder is not None


def test_html_builder_str() -> None:
    """Tests the __str__ method of the HTMLBuilder class."""
    old_method = HTMLBuilder.construct
    expected = "<This is a mock HTMLBuilder object>"
    HTMLBuilder.construct = lambda _: expected
    builder = HTMLBuilder()
    assert str(builder) == expected
    # Reset the method
    HTMLBuilder.construct = old_method


def test_html_builder_repr(builder: HTMLBuilder) -> None:
    """Tests the __repr__ method of the HTMLBuilder class."""
    expected = (
        "HTMLBuilder(attributes="
        "Attributes(attributes="
        "{'id': 'test', 'disabled': True, 'class': Classes()}"
        "))"
    )
    assert repr(builder) == expected
