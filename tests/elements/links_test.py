"""
Contains tests for the elements.links module.
"""

import pytest

from balisage.attributes import Attributes, Classes, Elements
from balisage.elements.links import Link

# MARK: Fixtures


@pytest.fixture
def sample_elements() -> Elements:
    """Creates a sample list of data."""
    return Elements("Test hyperlink")


@pytest.fixture
def link(sample_elements: Elements) -> Link:
    """Creates a sample link object that has classes and attributes."""
    return Link(
        elements=sample_elements,
        attributes=Attributes({"href": "#", "alt": "Hyperlink"}),
        classes=Classes("class 1", "class2"),
    )


# MARK: Link


def test_link_init(link: Link, sample_elements: Elements) -> None:
    """Tests the initialization of the Link class."""
    expected_attributes = Attributes(
        {
            "href": "#",
            "alt": "Hyperlink",
            "class": Classes("class 1", "class2"),
        }
    )
    assert link.elements == sample_elements
    assert link.attributes == expected_attributes
    assert link.classes == Classes("class 1", "class2")
    assert link.classes == Classes("class-1", "class2")
    assert link.tag == "a"
