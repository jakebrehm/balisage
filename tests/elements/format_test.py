"""
Contains tests for the elements.format module.
"""

import re

import pytest

from balisage.attributes import Attributes, Classes, Elements
from balisage.elements.format import HorizontalRule, LineBreak
from balisage.elements.image import Image

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
    assert line_break.tag == "br"

    # Verify that elements cannot be added
    message = "1 element would exceed the maximum number of elements (0)"
    with pytest.raises(ValueError, match=re.escape(message)):
        line_break.elements.add(HorizontalRule())


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

    # Verify that elements cannot be added
    message = "1 element would exceed the maximum number of elements (0)"
    with pytest.raises(ValueError, match=re.escape(message)):
        horizontal_rule.elements.add(HorizontalRule())


def test_horizontal_rule_construct(horizontal_rule: HorizontalRule) -> None:
    """Tests the construct method of the HorizontalRule class."""
    expected = "<hr id='test' disabled class='class-1 class2'>"
    assert horizontal_rule.construct() == expected
    assert HorizontalRule().construct() == "<hr>"
