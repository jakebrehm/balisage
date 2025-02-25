"""
Contains tests for the elements.text module.
"""

import pytest

from balisage.attributes import Attributes, Classes
from balisage.elements.text import (
    Heading1,
    Heading2,
    Heading3,
    Heading4,
    Heading5,
    Heading6,
    Paragraph,
    Text,
    TextType,
)

# MARK: Fixtures


@pytest.fixture
def sample_attributes() -> Attributes:
    """Creates a sample Attributes object."""
    return Attributes({"id": "test", "disabled": True})


@pytest.fixture
def sample_classes() -> Classes:
    """Creates a sample Classes object."""
    return Classes("class 1", "class2")


@pytest.fixture
def text(sample_attributes: Attributes, sample_classes: Classes) -> Text:
    """Creates a sample Text object that has classes and attributes."""
    return Text(
        "Test text",
        tag=TextType.H4,
        classes=sample_classes,
        attributes=sample_attributes,
    )


@pytest.fixture
def paragraph(sample_attributes: Attributes, sample_classes: Classes) -> Paragraph:
    """Creates a sample Paragraph object that has classes and attributes."""
    return Paragraph(
        "Test paragraph",
        classes=sample_classes,
        attributes=sample_attributes,
    )


@pytest.fixture
def heading1(sample_attributes: Attributes, sample_classes: Classes) -> Heading1:
    """Creates a sample Heading1 object that has classes and attributes."""
    return Heading1(
        "Test heading (size 1)",
        classes=sample_classes,
        attributes=sample_attributes,
    )


@pytest.fixture
def heading2(sample_attributes: Attributes, sample_classes: Classes) -> Heading2:
    """Creates a sample Heading2 object that has classes and attributes."""
    return Heading2(
        "Test heading (size 2)",
        classes=sample_classes,
        attributes=sample_attributes,
    )


@pytest.fixture
def heading3(sample_attributes: Attributes, sample_classes: Classes) -> Heading3:
    """Creates a sample Heading3 object that has classes and attributes."""
    return Heading3(
        "Test heading (size 3)",
        classes=sample_classes,
        attributes=sample_attributes,
    )


@pytest.fixture
def heading4(sample_attributes: Attributes, sample_classes: Classes) -> Heading4:
    """Creates a sample Heading4 object that has classes and attributes."""
    return Heading4(
        "Test heading (size 4)",
        classes=sample_classes,
        attributes=sample_attributes,
    )


@pytest.fixture
def heading5(sample_attributes: Attributes, sample_classes: Classes) -> Heading5:
    """Creates a sample Heading5 object that has classes and attributes."""
    return Heading5(
        "Test heading (size 5)",
        classes=sample_classes,
        attributes=sample_attributes,
    )


@pytest.fixture
def heading6(sample_attributes: Attributes, sample_classes: Classes) -> Heading6:
    """Creates a sample Heading6 object that has classes and attributes."""
    return Heading6(
        "Test heading (size 6)",
        classes=sample_classes,
        attributes=sample_attributes,
    )


# MARK: Text


def test_text_init(
    text: Text,
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> None:
    """Tests the initialization of the Text class."""

    # Test with arguments from fixture
    assert text == text
    assert text.attributes == sample_attributes
    assert text.classes == sample_classes
    assert text.text == "Test text"
    assert text.elements.max_elements == 1
    assert text.tag == TextType.H4.value
    assert Text("Test text").tag == TextType.P.value

    # Test with default arguments
    text = Text()
    assert text == text
    assert text.attributes == Attributes()
    assert text.classes == Classes()
    assert text.text == ""
    assert text.elements.max_elements == 1
    assert text.tag == TextType.P.value


def test_text_text(text: Text) -> None:
    """Tests the text property of the Text class."""
    assert text.text == "Test text"
    assert Text().text == ""


def test_text_set_text(text: Text) -> None:
    """Tests the set_text method of the Text class."""
    text.set("New text 1")
    assert text.text == "New text 1"
    text = Text()
    text.set("New text 2")
    assert text.text == "New text 2"


def test_text_clear(text: Text) -> None:
    """Tests the clear method of the Text class."""
    text.clear()
    assert text.text == ""


def test_text_construct(text: Text) -> None:
    """Tests the construct method of the Text class."""
    expected = "<h4 id='test' disabled class='class-1 class2'>Test text</h4>"
    assert text.construct() == expected
    assert Text("Some text").construct() == "<p>Some text</p>"
    assert Text().construct() == "<p></p>"


# MARK: Paragraph


def test_paragraph_init(
    paragraph: Paragraph,
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> None:
    """Tests the initialization of the Paragraph class."""
    assert paragraph == paragraph
    assert paragraph.attributes == sample_attributes
    assert paragraph.classes == sample_classes
    assert paragraph.text == "Test paragraph"
    assert paragraph.tag == TextType.P.value


# MARK: Heading1


def test_heading1_init(
    heading1: Heading1,
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> None:
    """Tests the initialization of the Heading1 class."""
    assert heading1 == heading1
    assert heading1.attributes == sample_attributes
    assert heading1.classes == sample_classes
    assert heading1.text == "Test heading (size 1)"
    assert heading1.tag == TextType.H1.value


# MARK: Heading2


def test_heading2_init(
    heading2: Heading2,
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> None:
    """Tests the initialization of the Heading2 class."""
    assert heading2 == heading2
    assert heading2.attributes == sample_attributes
    assert heading2.classes == sample_classes
    assert heading2.text == "Test heading (size 2)"
    assert heading2.tag == TextType.H2.value


# MARK: Heading3


def test_heading3_init(
    heading3: Heading3,
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> None:
    """Tests the initialization of the Heading3 class."""
    assert heading3 == heading3
    assert heading3.attributes == sample_attributes
    assert heading3.classes == sample_classes
    assert heading3.text == "Test heading (size 3)"
    assert heading3.tag == TextType.H3.value


# MARK: Heading4


def test_heading4_init(
    heading4: Heading4,
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> None:
    """Tests the initialization of the Heading4 class."""
    assert heading4 == heading4
    assert heading4.attributes == sample_attributes
    assert heading4.classes == sample_classes
    assert heading4.text == "Test heading (size 4)"
    assert heading4.tag == TextType.H4.value


# MARK: Heading5


def test_heading5_init(
    heading5: Heading5,
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> None:
    """Tests the initialization of the Heading5 class."""
    assert heading5 == heading5
    assert heading5.attributes == sample_attributes
    assert heading5.classes == sample_classes
    assert heading5.text == "Test heading (size 5)"
    assert heading5.tag == TextType.H5.value


# MARK: Heading6


def test_heading6_init(
    heading6: Heading6,
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> None:
    """Tests the initialization of the Heading1 class."""
    assert heading6 == heading6
    assert heading6.attributes == sample_attributes
    assert heading6.classes == sample_classes
    assert heading6.text == "Test heading (size 6)"
    assert heading6.tag == TextType.H6.value
