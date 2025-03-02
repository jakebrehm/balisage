"""
Contains tests for the elements.styles module.
"""

import pytest

from balisage.attributes import Attributes, Classes, Elements
from balisage.elements.format import HorizontalRule, LineBreak
from balisage.elements.image import Image
from balisage.elements.styles import Div, Span
from balisage.types import Element

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
def div(sample_elements: list[Element]) -> Div:
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


def test_div_add(div: Div, sample_elements: Elements) -> None:
    """Tests the add method of the Div class."""
    new_data = LineBreak()
    div.add(new_data)
    sample_elements.add(new_data)
    assert div.elements == sample_elements
    assert div.elements.elements == sample_elements.elements


def test_div_set(div: Div, sample_elements: Elements) -> None:
    """Tests the set method of the Div class."""
    new_data = [HorizontalRule(), LineBreak(attributes={"id": "test"})]
    div.set(*new_data)
    sample_elements._elements = new_data
    assert div.elements == sample_elements.elements
    assert div.elements.elements == sample_elements.elements


def test_div_insert(div: Div, sample_elements: Elements) -> None:
    """Tests the insert method of the Div class."""
    new_data = HorizontalRule()
    sample_elements._elements.insert(1, new_data)
    div.insert(1, new_data)
    assert div.elements == sample_elements
    assert div.elements.elements == sample_elements.elements
    assert len(div.elements) == len(sample_elements.elements)


def test_div_update(div: Div, sample_elements: Elements) -> None:
    """Tests the update method of the Div class."""
    new_data = LineBreak()
    sample_elements._elements[2] = new_data
    div.update(2, new_data)
    assert div.elements == sample_elements
    assert div.elements.elements == sample_elements.elements


def test_div_remove(div: Div, sample_elements: Elements) -> None:
    """Tests the remove method of the Div class."""
    div.remove(1)
    sample_elements.remove(1)
    assert div.elements == sample_elements
    assert div.elements.elements == sample_elements.elements
    assert len(div.elements) == len(sample_elements.elements)


def test_div_pop(div: Div, sample_elements: Elements) -> None:
    """Tests the pop method of the Div class."""

    # Pop with an integer argument
    div.pop(1)
    sample_elements._elements = (
        sample_elements.elements[:1] + sample_elements.elements[2:]
    )
    assert div.elements == sample_elements
    assert div.elements.elements == sample_elements.elements

    # Pop with a non-integer argument
    with pytest.raises(TypeError):
        div.pop("1")

    # Pop with no arguments
    div.pop()
    sample_elements._elements = sample_elements.elements[:-1]
    assert div.elements == sample_elements
    assert div.elements.elements == sample_elements.elements


def test_div_clear(div: Div) -> None:
    """Tests the clear method of the Div class."""
    div.clear()
    assert div.elements == Elements()
    assert div.elements.elements == []


def test_div_construct(div: Div) -> None:
    """Tests the construct method of the Div class."""
    expected = (
        "<div id='test' disabled class='class-1 class2'>"
        "<img src='image1.png'>"
        "<br>"
        "<img src='image2.png' alt='Image 2'>"
        "</div>"
    )
    assert div.construct() == expected
    assert Div().construct() == "<div></div>"


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
