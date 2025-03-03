"""
Contains tests for the elements.styles module.
"""

import pytest

from balisage.attributes import Attributes, Classes, Elements
from balisage.elements.format import HorizontalRule, LineBreak
from balisage.elements.image import Image
from balisage.elements.styles import Div, Span

# MARK: Fixtures


@pytest.fixture
def sample_elements() -> Elements:
    """Creates a sample list of data."""
    return Elements(
        Image(attributes=Attributes({"src": "image1.png"})),
        LineBreak(),
        Image(attributes=Attributes({"src": "image2.png", "alt": "Image 2"})),
    )


@pytest.fixture
def div(sample_elements: Elements) -> Div:
    """Creates a sample Div object that has classes and attributes."""
    return Div(
        elements=sample_elements,
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


@pytest.fixture
def span() -> Span:
    """Creates a sample Span object that has classes and attributes."""
    return Span(
        elements=Elements("Test text"),
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


# MARK: Div


def test_div_init(div: Div, sample_elements: Elements) -> None:
    """Tests the initialization of the Div class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert div.elements == sample_elements
    assert div.attributes == expected_attributes
    assert div.classes == Classes("class 1", "class2")
    assert div.classes == Classes("class-1", "class2")
    assert div.tag == "div"


# MARK: Span


def test_span_init(span: Span) -> None:
    """Tests the initialization of the Span class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert span.elements == Elements("Test text")
    assert span.elements == ["Test text"]
    assert span.attributes == expected_attributes
    assert span.classes == Classes("class 1", "class2")
    assert span.classes == Classes("class-1", "class2")
    assert span.tag == "span"

    # Test with a string
    span = Span("Test text")
    assert span.elements == Elements("Test text")
    assert span.elements == ["Test text"]
    assert span.attributes == Attributes()
    assert span.classes == Classes()
    assert span.tag == "span"

    # Test with no arguments
    span = Span()
    assert span.elements == Elements()
    assert span.attributes == Attributes()
    assert span.classes == Classes()
    assert span.tag == "span"


def test_span_set(span: Span, sample_elements: Elements) -> None:
    """Tests the set method of the Span class."""

    # Test with only one builder element
    new_data = HorizontalRule()
    span.set(new_data)
    sample_elements._elements = [new_data]
    assert span.elements == sample_elements.elements
    assert span.elements.elements == sample_elements.elements
    new_data = [HorizontalRule()]
    span.set(*new_data)
    sample_elements._elements = new_data
    assert span.elements == sample_elements.elements
    assert span.elements.elements == sample_elements.elements

    # Test with multiple builder elements
    new_data = [HorizontalRule(), LineBreak(attributes={"id": "test"})]
    span.set(*new_data)
    sample_elements._elements = new_data
    assert span.elements == sample_elements.elements
    assert span.elements.elements == sample_elements.elements

    # Test with only one string
    new_data = "Test string"
    span.set(new_data)
    sample_elements._elements = [new_data]
    assert span.elements == sample_elements.elements
    assert span.elements.elements == sample_elements.elements
    new_data = ["Test string"]
    span.set(*new_data)
    sample_elements._elements = new_data
    assert span.elements == sample_elements.elements
    assert span.elements.elements == sample_elements.elements

    # Test with only multiple strings
    new_data = ["Test string 1", "Test string 2"]
    span.set(*new_data)
    sample_elements._elements = new_data
    assert span.elements == sample_elements.elements
    assert span.elements.elements == sample_elements.elements

    # Test with a mix of builder and string elements
    new_data = [HorizontalRule(), "Test string"]
    span.set(*new_data)
    sample_elements._elements = new_data
    assert span.elements == sample_elements.elements
    assert span.elements.elements == sample_elements.elements


def test_span_add(span: Span) -> None:
    """Tests the __add__ method of the Span class."""

    # Try adding a string to the fixture
    assert (span + "Added text") == (
        "<span id='test' disabled class='class-1 class2'>Test text</span>Added text"
    )

    # Try adding a string to a fresh instance
    assert (Span() + "Added text") == "<span></span>Added text"

    # Try adding an invalid type to the fixture
    message = "Invalid type int for addition on Span; must be str"
    with pytest.raises(TypeError, match=message):
        span + 1

    # Try adding an invalid type to a fresh instance
    message = "Invalid type int for addition on Span; must be str"
    with pytest.raises(TypeError, match=message):
        Span() + 1


def test_span_radd(span: Span) -> None:
    """Tests the __radd__ method of the Span class."""

    # Try adding a string to the fixture
    assert ("Added text" + span) == (
        "Added text<span id='test' disabled class='class-1 class2'>Test text</span>"
    )

    # Try adding a string to a fresh instance
    assert ("Added text" + Span()) == "Added text<span></span>"

    # Try adding an invalid type to the fixture
    message = "Invalid type dict for reverse addition on Span; must be str"
    with pytest.raises(TypeError, match=message):
        {} + span

    # Try adding an invalid type to a fresh instance
    message = "Invalid type dict for reverse addition on Span; must be str"
    with pytest.raises(TypeError, match=message):
        {} + Span()


def test_span_construct(span: Span) -> None:
    """Tests the construct method of the Span class."""
    expected = "<span id='test' disabled class='class-1 class2'>Test text</span>"
    assert span.construct() == expected
    assert Span().construct() == "<span></span>"
