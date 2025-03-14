"""
Contains tests for the core module.
"""

import os
import pathlib
from copy import deepcopy

import pytest

from balisage.attributes import Attributes, Classes, Elements
from balisage.core import GenericElement, HTMLBuilder
from balisage.elements.basic import Page
from balisage.elements.format import HorizontalRule, LineBreak
from balisage.elements.image import Image
from balisage.elements.styles import Div
from balisage.elements.text import Heading1, Paragraph

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


@pytest.fixture
def sample_elements() -> Elements:
    """Creates a sample list of data."""
    return Elements(
        Image(attributes=Attributes({"src": "image1.png"})),
        LineBreak(),
        Image(attributes=Attributes({"src": "image2.png", "alt": "Image 2"})),
    )


@pytest.fixture
def generic_element(sample_elements: Elements) -> GenericElement:
    """Creates a sample GenericElement object that has classes and attributes."""
    return GenericElement(
        tag="div",
        elements=sample_elements,
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
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
    builder = HTMLBuilder(
        attributes=passed_attributes, classes=expected_classes
    )
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

    # Pass elements as single string
    passed_elements = "Test string"
    expected_elements = Elements(passed_elements)
    builder = HTMLBuilder(elements=passed_elements)
    assert builder.attributes == Attributes()
    assert builder.classes == Classes()
    assert builder.elements == expected_elements

    # Pass elements as single element
    passed_elements = Div()
    expected_elements = Elements(passed_elements)
    builder = HTMLBuilder(elements=passed_elements)
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

    # Pass invalid values for elements
    invalid_values = [
        (1, "int"),
        (2.0, "float"),
        (True, "bool"),
        ({}, "dict"),
        ((), "tuple"),
    ]
    for invalid_value, invalid_type in invalid_values:
        message = f"Invalid type {invalid_type} for Elements"
        with pytest.raises(TypeError, match=message):
            HTMLBuilder(elements=invalid_value)


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
        filepath = os.path.join(
            current_directory, r"_data/prettify_indent_2.html"
        )
        with open(filepath, "r", encoding="utf-8") as f:
            expected = f.read()
        assert page.prettify() == expected

        # Test with a different indent
        filepath = os.path.join(
            current_directory, r"_data/prettify_indent_4.html"
        )
        with open(filepath, "r", encoding="utf-8") as f:
            expected = f.read()
        assert page.prettify(indent=4) == expected

    else:
        filepath = os.path.join(
            current_directory, r"_data/prettify_indent_0.html"
        )
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

    # Try using the fixture
    expected = (
        "HTMLBuilder(attributes="
        "Attributes(attributes="
        "{'id': 'test', 'disabled': True, 'class': Classes()}"
        "))"
    )
    assert repr(builder) == expected

    # Try with no attributes
    builder.attributes.clear()
    assert repr(builder) == "HTMLBuilder()"


# MARK: GenericElement


def test_generic_element_init(
    generic_element: GenericElement, sample_elements: Elements
) -> None:
    """Tests the initialization of the GenericElement class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert generic_element.elements == sample_elements
    assert generic_element.attributes == expected_attributes
    assert generic_element.classes == Classes("class 1", "class2")
    assert generic_element.classes == Classes("class-1", "class2")
    assert generic_element.tag == "div"


def test_generic_element_add(
    generic_element: GenericElement, sample_elements: Elements
) -> None:
    """Tests the add method of the GenericElement class."""
    new_data = LineBreak()
    generic_element.add(new_data)
    sample_elements.add(new_data)
    assert generic_element.elements == sample_elements
    assert generic_element.elements.elements == sample_elements.elements


def test_generic_element_set(
    generic_element: GenericElement, sample_elements: Elements
) -> None:
    """Tests the set method of the GenericElement class."""

    # Test with only one builder element
    new_data = HorizontalRule()
    generic_element.set(new_data)
    sample_elements._elements = [new_data]
    assert generic_element.elements == sample_elements.elements
    assert generic_element.elements.elements == sample_elements.elements
    new_data = [HorizontalRule()]
    generic_element.set(*new_data)
    sample_elements._elements = new_data
    assert generic_element.elements == sample_elements.elements
    assert generic_element.elements.elements == sample_elements.elements

    # Test with multiple builder elements
    new_data = [HorizontalRule(), LineBreak(attributes={"id": "test"})]
    generic_element.set(*new_data)
    sample_elements._elements = new_data
    assert generic_element.elements == sample_elements.elements
    assert generic_element.elements.elements == sample_elements.elements

    # Test with only one string
    new_data = "Test string"
    generic_element.set(new_data)
    sample_elements._elements = [new_data]
    assert generic_element.elements == sample_elements.elements
    assert generic_element.elements.elements == sample_elements.elements
    new_data = ["Test string"]
    generic_element.set(*new_data)
    sample_elements._elements = new_data
    assert generic_element.elements == sample_elements.elements
    assert generic_element.elements.elements == sample_elements.elements

    # Test with only multiple strings
    new_data = ["Test string 1", "Test string 2"]
    generic_element.set(*new_data)
    sample_elements._elements = new_data
    assert generic_element.elements == sample_elements.elements
    assert generic_element.elements.elements == sample_elements.elements

    # Test with a mix of builder and string elements
    new_data = [HorizontalRule(), "Test string"]
    generic_element.set(*new_data)
    sample_elements._elements = new_data
    assert generic_element.elements == sample_elements.elements
    assert generic_element.elements.elements == sample_elements.elements


def test_generic_element_insert(
    generic_element: GenericElement, sample_elements: Elements
) -> None:
    """Tests the insert method of the GenericElement class."""
    new_data = HorizontalRule()
    sample_elements._elements.insert(1, new_data)
    generic_element.insert(1, new_data)
    assert generic_element.elements == sample_elements
    assert generic_element.elements.elements == sample_elements.elements
    assert len(generic_element.elements) == len(sample_elements.elements)


def test_generic_element_update(
    generic_element: GenericElement, sample_elements: Elements
) -> None:
    """Tests the update method of the GenericElement class."""
    new_data = LineBreak()
    sample_elements._elements[2] = new_data
    generic_element.update(2, new_data)
    assert generic_element.elements == sample_elements
    assert generic_element.elements.elements == sample_elements.elements


def test_generic_element_remove(
    generic_element: GenericElement, sample_elements: Elements
) -> None:
    """Tests the remove method of the GenericElement class."""
    generic_element.remove(1)
    sample_elements.remove(1)
    assert generic_element.elements == sample_elements
    assert generic_element.elements.elements == sample_elements.elements
    assert len(generic_element.elements) == len(sample_elements.elements)


def test_generic_element_pop(
    generic_element: GenericElement, sample_elements: Elements
) -> None:
    """Tests the pop method of the GenericElement class."""

    # Pop with an integer argument
    generic_element.pop(1)
    sample_elements._elements = (
        sample_elements.elements[:1] + sample_elements.elements[2:]
    )
    assert generic_element.elements == sample_elements
    assert generic_element.elements.elements == sample_elements.elements

    # Pop with a non-integer argument
    with pytest.raises(TypeError):
        generic_element.pop("1")

    # Pop with no arguments
    generic_element.pop()
    sample_elements._elements = sample_elements.elements[:-1]
    assert generic_element.elements == sample_elements
    assert generic_element.elements.elements == sample_elements.elements


def test_generic_element_clear(generic_element: GenericElement) -> None:
    """Tests the clear method of the GenericElement class."""
    generic_element.clear()
    assert generic_element.elements == Elements()
    assert generic_element.elements.elements == []


def test_generic_element_construct(generic_element: GenericElement) -> None:
    """Tests the construct method of the GenericElement class."""
    expected = (
        "<div id='test' disabled class='class-1 class2'>"
        "<img src='image1.png'>"
        "<br>"
        "<img src='image2.png' alt='Image 2'>"
        "</div>"
    )
    assert generic_element.construct() == expected
    assert GenericElement("div").construct() == "<div></div>"


def test_generic_element_ladd(generic_element: GenericElement) -> None:
    """Tests the __add__ method of the GenericElement class."""

    # Try adding a string to the fixture
    assert (generic_element + "Added text") == (
        "<div id='test' disabled class='class-1 class2'>"
        "<img src='image1.png'>"
        "<br>"
        "<img src='image2.png' alt='Image 2'>"
        "</div>"
        "Added text"
    )

    # Try adding a string to a fresh instance
    assert (GenericElement("div") + "Added text") == "<div></div>Added text"

    # Try adding an invalid type to the fixture
    message = "Invalid type int for addition on GenericElement; must be str"
    with pytest.raises(TypeError, match=message):
        generic_element + 1

    # Try adding an invalid type to a fresh instance
    message = "Invalid type int for addition on GenericElement; must be str"
    with pytest.raises(TypeError, match=message):
        GenericElement("div") + 1


def test_generic_element_radd(generic_element: GenericElement) -> None:
    """Tests the __radd__ method of the GenericElement class."""

    # Try adding a string to the fixture
    assert ("Added text" + generic_element) == (
        "Added text"
        "<div id='test' disabled class='class-1 class2'>"
        "<img src='image1.png'>"
        "<br>"
        "<img src='image2.png' alt='Image 2'>"
        "</div>"
    )

    # Try adding a string to a fresh instance
    assert ("Added text" + GenericElement("div")) == "Added text<div></div>"

    # Try adding an invalid type to the fixture
    message = (
        "Invalid type dict for reverse addition on GenericElement; must be str"
    )
    with pytest.raises(TypeError, match=message):
        {} + generic_element

    # Try adding an invalid type to a fresh instance
    message = (
        "Invalid type dict for reverse addition on GenericElement; must be str"
    )
    with pytest.raises(TypeError, match=message):
        {} + GenericElement("div")
