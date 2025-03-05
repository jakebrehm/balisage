"""
Contains tests for the elements.styles module.
"""

import pytest

from balisage.attributes import Attributes, Classes, Elements
from balisage.elements.format import LineBreak
from balisage.elements.image import Image
from balisage.elements.styles import (
    Bold,
    Div,
    Emphasis,
    Italics,
    Span,
    Strikethrough,
    Strong,
    Subscript,
    Superscript,
    Underline,
)

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


@pytest.fixture
def bold() -> Bold:
    """Creates a sample Bold object that has classes and attributes."""
    return Bold(
        elements=Elements("Test text"),
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


@pytest.fixture
def strong() -> Strong:
    """Creates a sample Strong object that has classes and attributes."""
    return Strong(
        elements=Elements("Test text"),
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


@pytest.fixture
def italics() -> Italics:
    """Creates a sample Italics object that has classes and attributes."""
    return Italics(
        elements=Elements("Test text"),
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


@pytest.fixture
def emphasis() -> Emphasis:
    """Creates a sample Emphasis object that has classes and attributes."""
    return Emphasis(
        elements=Elements("Test text"),
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


@pytest.fixture
def underline() -> Underline:
    """Creates a sample Underline object that has classes and attributes."""
    return Underline(
        elements=Elements("Test text"),
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


@pytest.fixture
def strikethrough() -> Strikethrough:
    """Creates a sample Strikethrough object that has classes and attributes."""
    return Strikethrough(
        elements=Elements("Test text"),
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


@pytest.fixture
def subscript() -> Subscript:
    """Creates a sample Subscript object that has classes and attributes."""
    return Subscript(
        elements=Elements("Test text"),
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


@pytest.fixture
def superscript() -> Superscript:
    """Creates a sample Superscript object that has classes and attributes."""
    return Superscript(
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


# MARK: Bold


def test_bold_init(bold: Bold) -> None:
    """Tests the initialization of the Bold class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert bold.elements == Elements("Test text")
    assert bold.elements == ["Test text"]
    assert bold.attributes == expected_attributes
    assert bold.classes == Classes("class 1", "class2")
    assert bold.classes == Classes("class-1", "class2")
    assert bold.tag == "b"

    # Test with a string
    bold = Bold("Test text")
    assert bold.elements == Elements("Test text")
    assert bold.elements == ["Test text"]
    assert bold.attributes == Attributes()
    assert bold.classes == Classes()
    assert bold.tag == "b"

    # Test with no arguments
    bold = Bold()
    assert bold.elements == Elements()
    assert bold.attributes == Attributes()
    assert bold.classes == Classes()
    assert bold.tag == "b"


# MARK: Strong


def test_strong_init(strong: Strong) -> None:
    """Tests the initialization of the Strong class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert strong.elements == Elements("Test text")
    assert strong.elements == ["Test text"]
    assert strong.attributes == expected_attributes
    assert strong.classes == Classes("class 1", "class2")
    assert strong.classes == Classes("class-1", "class2")
    assert strong.tag == "strong"

    # Test with a string
    strong = Strong("Test text")
    assert strong.elements == Elements("Test text")
    assert strong.elements == ["Test text"]
    assert strong.attributes == Attributes()
    assert strong.classes == Classes()
    assert strong.tag == "strong"

    # Test with no arguments
    strong = Strong()
    assert strong.elements == Elements()
    assert strong.attributes == Attributes()
    assert strong.classes == Classes()
    assert strong.tag == "strong"


# MARK: Italics


def test_italics_init(italics: Italics) -> None:
    """Tests the initialization of the Italics class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert italics.elements == Elements("Test text")
    assert italics.elements == ["Test text"]
    assert italics.attributes == expected_attributes
    assert italics.classes == Classes("class 1", "class2")
    assert italics.classes == Classes("class-1", "class2")
    assert italics.tag == "i"

    # Test with a string
    italics = Italics("Test text")
    assert italics.elements == Elements("Test text")
    assert italics.elements == ["Test text"]
    assert italics.attributes == Attributes()
    assert italics.classes == Classes()
    assert italics.tag == "i"

    # Test with no arguments
    italics = Italics()
    assert italics.elements == Elements()
    assert italics.attributes == Attributes()
    assert italics.classes == Classes()
    assert italics.tag == "i"


# MARK: Emphasis


def test_emphasis_init(emphasis: Emphasis) -> None:
    """Tests the initialization of the Emphasis class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert emphasis.elements == Elements("Test text")
    assert emphasis.elements == ["Test text"]
    assert emphasis.attributes == expected_attributes
    assert emphasis.classes == Classes("class 1", "class2")
    assert emphasis.classes == Classes("class-1", "class2")
    assert emphasis.tag == "em"

    # Test with a string
    emphasis = Emphasis("Test text")
    assert emphasis.elements == Elements("Test text")
    assert emphasis.elements == ["Test text"]
    assert emphasis.attributes == Attributes()
    assert emphasis.classes == Classes()
    assert emphasis.tag == "em"

    # Test with no arguments
    emphasis = Emphasis()
    assert emphasis.elements == Elements()
    assert emphasis.attributes == Attributes()
    assert emphasis.classes == Classes()
    assert emphasis.tag == "em"


# MARK: Underline


def test_underline_init(underline: Underline) -> None:
    """Tests the initialization of the Underline class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert underline.elements == Elements("Test text")
    assert underline.elements == ["Test text"]
    assert underline.attributes == expected_attributes
    assert underline.classes == Classes("class 1", "class2")
    assert underline.classes == Classes("class-1", "class2")
    assert underline.tag == "u"

    # Test with a string
    underline = Underline("Test text")
    assert underline.elements == Elements("Test text")
    assert underline.elements == ["Test text"]
    assert underline.attributes == Attributes()
    assert underline.classes == Classes()
    assert underline.tag == "u"

    # Test with no arguments
    underline = Underline()
    assert underline.elements == Elements()
    assert underline.attributes == Attributes()
    assert underline.classes == Classes()
    assert underline.tag == "u"


# MARK: Strikethrough


def test_strikethrough_init(strikethrough: Strikethrough) -> None:
    """Tests the initialization of the Strikethrough class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert strikethrough.elements == Elements("Test text")
    assert strikethrough.elements == ["Test text"]
    assert strikethrough.attributes == expected_attributes
    assert strikethrough.classes == Classes("class 1", "class2")
    assert strikethrough.classes == Classes("class-1", "class2")
    assert strikethrough.tag == "s"

    # Test with a string
    strikethrough = Strikethrough("Test text")
    assert strikethrough.elements == Elements("Test text")
    assert strikethrough.elements == ["Test text"]
    assert strikethrough.attributes == Attributes()
    assert strikethrough.classes == Classes()
    assert strikethrough.tag == "s"

    # Test with no arguments
    strikethrough = Strikethrough()
    assert strikethrough.elements == Elements()
    assert strikethrough.attributes == Attributes()
    assert strikethrough.classes == Classes()
    assert strikethrough.tag == "s"


# MARK: Subscript


def test_subscript_init(subscript: Subscript) -> None:
    """Tests the initialization of the Subscript class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert subscript.elements == Elements("Test text")
    assert subscript.elements == ["Test text"]
    assert subscript.attributes == expected_attributes
    assert subscript.classes == Classes("class 1", "class2")
    assert subscript.classes == Classes("class-1", "class2")
    assert subscript.tag == "sub"

    # Test with a string
    subscript = Subscript("Test text")
    assert subscript.elements == Elements("Test text")
    assert subscript.elements == ["Test text"]
    assert subscript.attributes == Attributes()
    assert subscript.classes == Classes()
    assert subscript.tag == "sub"

    # Test with no arguments
    subscript = Subscript()
    assert subscript.elements == Elements()
    assert subscript.attributes == Attributes()
    assert subscript.classes == Classes()
    assert subscript.tag == "sub"


# MARK: Superscript


def test_superscript_init(superscript: Superscript) -> None:
    """Tests the initialization of the Superscript class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert superscript.elements == Elements("Test text")
    assert superscript.elements == ["Test text"]
    assert superscript.attributes == expected_attributes
    assert superscript.classes == Classes("class 1", "class2")
    assert superscript.classes == Classes("class-1", "class2")
    assert superscript.tag == "sup"

    # Test with a string
    superscript = Superscript("Test text")
    assert superscript.elements == Elements("Test text")
    assert superscript.elements == ["Test text"]
    assert superscript.attributes == Attributes()
    assert superscript.classes == Classes()
    assert superscript.tag == "sup"

    # Test with no arguments
    superscript = Superscript()
    assert superscript.elements == Elements()
    assert superscript.attributes == Attributes()
    assert superscript.classes == Classes()
    assert superscript.tag == "sup"
