"""
Contains tests for the elements.styles module.
"""

import pytest

from balisage.attributes import Attributes, Classes, Elements
from balisage.elements.format import HorizontalRule, LineBreak
from balisage.elements.image import Image
from balisage.elements.styles import Div
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
