"""
Contains tests for the elements.basic module.
"""

import pytest

from balisage.attributes import Attributes, Classes, Elements
from balisage.elements.basic import Page
from balisage.elements.format import HorizontalRule, LineBreak
from balisage.elements.styles import Div
from balisage.elements.text import Heading1, Paragraph

# MARK: Fixtures


@pytest.fixture
def sample_elements() -> Elements:
    """Creates a sample list of data."""
    return Elements(
        Heading1("Title", attributes=Attributes({"id": "title"})),
        HorizontalRule(),
        Div(
            elements=Elements(
                Paragraph("Test paragraph 1", classes=Classes("subtitle")),
                LineBreak(),
                Paragraph("Test paragraph 2"),
            )
        ),
    )


@pytest.fixture
def page(sample_elements: Elements) -> Page:
    """Creates a sample Page object."""
    return Page(
        title="Test page",
        elements=sample_elements,
        lang="fr",
        charset="UTF-16",
        stylesheets=["style1.css", "style2.css"],
    )


# MARK: Page


def test_page_init(page: Page, sample_elements: Elements) -> None:
    """Tests the initialization of the Page class."""

    # Test with arguments from fixture
    assert page.elements == sample_elements
    assert page.tag == "html"
    assert page.title == "Test page"
    assert page.lang == "fr"
    assert page.charset == "UTF-16"
    assert page._stylesheets == ["style1.css", "style2.css"]

    # Test with passing minimal arguments
    page = Page("Test page")
    assert page.elements == Elements()
    assert page.tag == "html"
    assert page.title == "Test page"
    assert page.lang == "en"
    assert page.charset == "UTF-8"
    assert page._stylesheets == []

    # Test with passing some arguments as None
    page = Page("Test page", lang=None, charset=None)
    assert page.elements == Elements()
    assert page.tag == "html"
    assert page.title == "Test page"
    assert page.lang is None
    assert page.charset is None
    assert page._stylesheets == []

    # Test with no arguments
    with pytest.raises(TypeError):
        page = Page()


def test_page_title(page: Page) -> None:
    """Tests the title property of the Page class."""

    # Test getter property
    assert page.title == "Test page"

    # Test setter property
    page.title = "New title"
    assert page.title == "New title"

    # Test with invalid type
    message = "title must be a non-empty string"
    invalid_values = ["", 1, 2.0, True, False, tuple(), dict(), None]
    for invalid_value in invalid_values:
        with pytest.raises(TypeError, match=message):
            page.title = invalid_value


def test_page_stylesheets(page: Page) -> None:
    """Tests the stylesheets property of the Page class."""

    # Test getter property
    assert page.stylesheets == ["style1.css", "style2.css"]

    # Test setter property
    page.stylesheets = ["style1.css", "style2.css"]
    assert page.stylesheets == ["style1.css", "style2.css"]

    # Test ability to use property as you would a list
    page.stylesheets.append("style3.css")
    assert page.stylesheets == ["style1.css", "style2.css", "style3.css"]
    page.stylesheets.clear()
    assert page.stylesheets == []

    # Test for stylesheets of different types
    message = "stylesheets must be provided as a list of strings"
    invalid_values = ["style.css", 1, 2.0, True, False, tuple(), dict(), [None]]
    for invalid_value in invalid_values:
        with pytest.raises(TypeError, match=message):
            Page(title="Test title", stylesheets=invalid_value)
    page = Page(title="Test title", stylesheets=[])
    assert page.stylesheets == []


def test_page_add(page: Page, sample_elements: Elements) -> None:
    """Tests the add method of the Page class."""
    new_data = LineBreak()
    page.add(new_data)
    sample_elements.add(new_data)
    assert page.elements == sample_elements
    assert page.elements.elements == sample_elements.elements


def test_page_set(page: Page, sample_elements: Elements) -> None:
    """Tests the set method of the Page class."""
    new_data = [HorizontalRule(), LineBreak(attributes={"id": "test"})]
    page.set(*new_data)
    sample_elements._elements = new_data
    assert page.elements == sample_elements.elements
    assert page.elements.elements == sample_elements.elements


def test_page_insert(page: Page, sample_elements: Elements) -> None:
    """Tests the insert method of the Page class."""
    new_data = HorizontalRule()
    sample_elements._elements.insert(1, new_data)
    page.insert(1, new_data)
    assert page.elements == sample_elements
    assert page.elements.elements == sample_elements.elements
    assert len(page.elements) == len(sample_elements.elements)


def test_page_update(page: Page, sample_elements: Elements) -> None:
    """Tests the update method of the Page class."""
    new_data = LineBreak()
    sample_elements._elements[2] = new_data
    page.update(2, new_data)
    assert page.elements == sample_elements
    assert page.elements.elements == sample_elements.elements


def test_page_remove(page: Page, sample_elements: Elements) -> None:
    """Tests the remove method of the Page class."""
    page.remove(1)
    sample_elements.remove(1)
    assert page.elements == sample_elements
    assert page.elements.elements == sample_elements.elements
    assert len(page.elements) == len(sample_elements.elements)


def test_page_pop(page: Page, sample_elements: Elements) -> None:
    """Tests the pop method of the Page class."""

    # Pop with an integer argument
    page.pop(1)
    sample_elements._elements = (
        sample_elements.elements[:1] + sample_elements.elements[2:]
    )
    assert page.elements == sample_elements
    assert page.elements.elements == sample_elements.elements

    # Pop with a non-integer argument
    with pytest.raises(TypeError):
        page.pop("1")

    # Pop with no arguments
    page.pop()
    sample_elements._elements = sample_elements.elements[:-1]
    assert page.elements == sample_elements
    assert page.elements.elements == sample_elements.elements


def test_page_clear(page: Page) -> None:
    """Tests the clear method of the Page class."""
    page.clear()
    assert page.elements == Elements()
    assert page.elements.elements == []


def test_page_construct(page: Page) -> None:
    """Tests the construct method of the Page class."""

    # Define expected HTML
    boilerplate = (
        "<!DOCTYPE html>"
        "<html{language}>"
        "<head>"
        "{charset}"
        "<title>{title}</title>"
        "{stylesheets}"
        "</head>"
        "<body>"
        "{body}"
        "</body>"
        "</html>"
    )

    # Test with arguments from fixture
    assert page.construct() == boilerplate.format(
        language=" lang='fr'",
        charset="<meta charset='UTF-16'>",
        title="Test page",
        stylesheets=(
            "<link rel='stylesheet' href='style1.css'>"
            "<link rel='stylesheet' href='style2.css'>"
        ),
        body=(
            "<h1 id='title'>Title</h1>"
            "<hr>"
            "<div>"
            "<p class='subtitle'>Test paragraph 1</p>"
            "<br>"
            "<p>Test paragraph 2</p>"
            "</div>"
        ),
    )

    # Test with an instance made with minimal arguments
    assert Page("Test page").construct() == boilerplate.format(
        language=" lang='en'",
        charset="<meta charset='UTF-8'>",
        title="Test page",
        stylesheets="",
        body="",
    )

    # Test with charset passed as None
    assert Page("Test page", charset=None).construct() == boilerplate.format(
        language=" lang='en'",
        charset="",
        title="Test page",
        stylesheets="",
        body="",
    )

    # Test with lang passed as None
    assert Page("Test page", lang=None).construct() == boilerplate.format(
        language="",
        charset="<meta charset='UTF-8'>",
        title="Test page",
        stylesheets="",
        body="",
    )
