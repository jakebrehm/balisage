"""
Contains tests for the elements.image module.
"""

import pytest

from html_builder.attributes import Attributes, Classes
from html_builder.elements.image import Image

# MARK: Fixtures


@pytest.fixture
def image() -> Image:
    """Creates a sample Image object that has classes and attributes."""
    return Image(
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


# MARK: Image


def test_image_init(image: Image) -> None:
    """Tests the initialization of the Image class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert image.attributes == expected_attributes
    assert image.classes == Classes("class 1", "class2")
    assert image.classes == Classes("class-1", "class2")
    assert image.tag == "img"


def test_image_construct(image: Image) -> None:
    """Tests the construct method of the Image class."""
    expected = "<img id='test' disabled class='class-1 class2'>"
    assert image.construct() == expected
