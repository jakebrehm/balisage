"""
Contains tests for the elements.format module.
"""

import pytest

from html_builder.attributes import Attributes, Classes, Element, Elements
from html_builder.elements.format import Div, HorizontalRule, LineBreak
from html_builder.elements.image import Image

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
def line_break() -> LineBreak:
    """Creates a sample LineBreak object that has classes and attributes."""
    return LineBreak(
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


@pytest.fixture
def horizontal_rule() -> HorizontalRule:
    """Creates a sample HorizontalRule object that has classes and attributes."""
    return HorizontalRule(
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


@pytest.fixture
def div(sample_elements: list[Element]) -> Div:
    """Creates a sample Div object that has classes and attributes."""
    return Div(
        elements=sample_elements,
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


# MARK: Line Break


def test_line_break_init(line_break: LineBreak) -> None:
    """Tests the initialization of the LineBreak class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert line_break.attributes == expected_attributes
    assert line_break.classes == Classes("class 1", "class2")
    assert line_break.classes == Classes("class-1", "class2")
    assert line_break.tag == "br"


def test_line_break_construct(line_break: LineBreak) -> None:
    """Tests the construct method of the LineBreak class."""
    expected = "<br id='test' disabled class='class-1 class2'>"
    assert line_break.construct() == expected
    assert LineBreak().construct() == "<br>"


# MARK: Horizontal Rule


def test_horizontal_rule_init(horizontal_rule: HorizontalRule) -> None:
    """Tests the initialization of the HorizontalRule class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert horizontal_rule.attributes == expected_attributes
    assert horizontal_rule.classes == Classes("class 1", "class2")
    assert horizontal_rule.classes == Classes("class-1", "class2")
    assert horizontal_rule.tag == "hr"


def test_horizontal_rule_construct(horizontal_rule: HorizontalRule) -> None:
    """Tests the construct method of the HorizontalRule class."""
    expected = "<hr id='test' disabled class='class-1 class2'>"
    assert horizontal_rule.construct() == expected
    assert HorizontalRule().construct() == "<hr>"


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


def test_div_add_data(div: Div, sample_elements: Elements) -> None:
    """Tests the add_data method of the Div class."""
    new_data = LineBreak()
    div.elements.add(new_data)
    sample_elements.add(new_data)
    assert div.elements == sample_elements.elements
    assert div.elements.elements == sample_elements.elements


def test_div_set_data(div: Div) -> None:
    """Tests the set_data method of the Div class."""
    new_data = [HorizontalRule(), LineBreak(attributes={"id": "test"})]
    div.elements.set(*new_data)
    assert div.elements == new_data


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
