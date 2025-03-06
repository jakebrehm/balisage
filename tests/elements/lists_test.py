"""
Contains tests for the elements.lists module.
"""

import pytest

from balisage.attributes import Attributes, Classes, Elements
from balisage.elements.lists import ListItem, OrderedList, UnorderedList
from balisage.elements.styles import Div

# MARK: Fixtures


@pytest.fixture
def sample_elements() -> Elements:
    """Creates a sample list of data."""
    return Elements(Div(elements=Elements("Test text")))


@pytest.fixture
def list_item(sample_elements: Elements) -> ListItem:
    """Creates a sample list item object with classes and attributes."""
    return ListItem(
        elements=sample_elements,
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


@pytest.fixture
def ordered_list() -> OrderedList:
    """Creates a sample ordered list object with classes and attributes."""
    return OrderedList(
        elements=Elements(
            ListItem(elements=Elements("First item")),
            ListItem(elements=Elements("Second item")),
            ListItem(elements=Elements("Third item")),
        ),
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


@pytest.fixture
def unordered_list() -> UnorderedList:
    """Creates a sample unordered list object with classes and attributes."""
    return UnorderedList(
        elements=Elements(
            ListItem(elements=Elements("First item")),
            ListItem(elements=Elements("Second item")),
            ListItem(elements=Elements("Third item")),
        ),
        attributes=Attributes({"id": "test", "disabled": True}),
        classes=Classes("class 1", "class2"),
    )


# MARK: List Item


def test_list_item_init(
    list_item: ListItem, sample_elements: Elements
) -> None:
    """Tests the initialization of the ListItem class."""
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert list_item.elements == sample_elements
    assert list_item.attributes == expected_attributes
    assert list_item.classes == Classes("class 1", "class2")
    assert list_item.classes == Classes("class-1", "class2")
    assert list_item.tag == "li"


# MARK: Ordered List


def test_ordered_list_init(ordered_list: OrderedList) -> None:
    """Tests the initialization of the OrderedList class."""

    # Test with valid elements
    expected_elements = Elements(
        ListItem(elements=Elements("First item")),
        ListItem(elements=Elements("Second item")),
        ListItem(elements=Elements("Third item")),
    )
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert ordered_list.elements == expected_elements
    assert ordered_list.attributes == expected_attributes
    assert ordered_list.classes == Classes("class 1", "class2")
    assert ordered_list.classes == Classes("class-1", "class2")
    assert ordered_list.tag == "ol"

    # Test with invalid elements
    message = "All elements of OrderedList must be of type ListItem"
    with pytest.raises(TypeError, match=message):
        OrderedList(
            elements=Elements(
                ListItem(elements=Elements("First item")),
                "Invalid element",
                ListItem(elements=Elements("Third item")),
            )
        )


def test_ordered_list_add(ordered_list: OrderedList) -> None:
    """Tests the add method of the OrderedList class."""

    # Add a single valid element
    new_element = ListItem(elements=Elements("New item"))
    ordered_list.add(new_element)
    expected_elements = Elements(
        ListItem(elements=Elements("First item")),
        ListItem(elements=Elements("Second item")),
        ListItem(elements=Elements("Third item")),
        ListItem(elements=Elements("New item")),
    )
    assert ordered_list.elements == expected_elements

    # Add multiple valid elements
    new_elements = [
        ListItem(elements=Elements("New item 1")),
        ListItem(elements=Elements("New item 2")),
    ]
    ordered_list.add(*new_elements)
    expected_elements = Elements(
        ListItem(elements=Elements("First item")),
        ListItem(elements=Elements("Second item")),
        ListItem(elements=Elements("Third item")),
        ListItem(elements=Elements("New item")),
        ListItem(elements=Elements("New item 1")),
        ListItem(elements=Elements("New item 2")),
    )
    assert ordered_list.elements == expected_elements

    # Add invalid elements
    invalid_elements = [
        "Invalid element",
        1,
        2.0,
        True,
        False,
        tuple(),
        dict(),
        None,
    ]
    for invalid_element in invalid_elements:
        class_name = invalid_element.__class__.__name__
        message = f"Expected ListItem object, got {class_name}"
        with pytest.raises(TypeError, match=message):
            ordered_list.add(invalid_element)


def test_ordered_list_set(ordered_list: OrderedList) -> None:
    """Tests the set method of the OrderedList class."""

    # Set a single valid element
    new_element = ListItem(elements=Elements("New item"))
    ordered_list.set(new_element)
    expected_elements = Elements(
        ListItem(elements=Elements("New item")),
    )
    assert ordered_list.elements == expected_elements

    # Set multiple valid elements
    new_elements = [
        ListItem(elements=Elements("New item 1")),
        ListItem(elements=Elements("New item 2")),
    ]
    ordered_list.set(*new_elements)
    expected_elements = Elements(
        ListItem(elements=Elements("New item 1")),
        ListItem(elements=Elements("New item 2")),
    )
    assert ordered_list.elements == expected_elements

    # Set invalid elements
    invalid_elements = [
        "Invalid element",
        1,
        2.0,
        True,
        False,
        tuple(),
        dict(),
        None,
    ]
    for invalid_element in invalid_elements:
        class_name = invalid_element.__class__.__name__
        message = f"Expected ListItem object, got {class_name}"
        with pytest.raises(TypeError, match=message):
            ordered_list.set(invalid_element)


def test_ordered_list_insert(ordered_list: OrderedList) -> None:
    """Tests the insert method of the OrderedList class."""

    # Insert a valid element
    new_element = ListItem(elements=Elements("New item"))
    ordered_list.insert(2, new_element)
    expected_elements = Elements(
        ListItem(elements=Elements("First item")),
        ListItem(elements=Elements("Second item")),
        ListItem(elements=Elements("New item")),
        ListItem(elements=Elements("Third item")),
    )
    assert ordered_list.elements == expected_elements

    # Insert invalid elements
    invalid_elements = [
        "Invalid element",
        1,
        2.0,
        True,
        False,
        tuple(),
        dict(),
        None,
    ]
    for invalid_element in invalid_elements:
        class_name = invalid_element.__class__.__name__
        message = f"Expected ListItem object, got {class_name}"
        with pytest.raises(TypeError, match=message):
            ordered_list.insert(0, invalid_element)


def test_ordered_list_update(ordered_list: OrderedList) -> None:
    """Tests the update method of the OrderedList class."""

    # Update with a valid element
    new_element = ListItem(elements=Elements("New item"))
    ordered_list.update(1, new_element)
    expected_elements = Elements(
        ListItem(elements=Elements("First item")),
        ListItem(elements=Elements("New item")),
        ListItem(elements=Elements("Third item")),
    )
    assert ordered_list.elements == expected_elements

    # Update with invalid elements
    invalid_elements = [
        "Invalid element",
        1,
        2.0,
        True,
        False,
        tuple(),
        dict(),
        None,
    ]
    for invalid_element in invalid_elements:
        class_name = invalid_element.__class__.__name__
        message = f"Expected ListItem object, got {class_name}"
        with pytest.raises(TypeError, match=message):
            ordered_list.update(0, invalid_element)


# MARK: Unordered List


def test_unordered_list_init(unordered_list: UnorderedList) -> None:
    """Tests the initialization of the UnorderedList class."""

    # Test with valid elements
    expected_elements = Elements(
        ListItem(elements=Elements("First item")),
        ListItem(elements=Elements("Second item")),
        ListItem(elements=Elements("Third item")),
    )
    expected_attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes("class 1", "class2"),
        }
    )
    assert unordered_list.elements == expected_elements
    assert unordered_list.attributes == expected_attributes
    assert unordered_list.classes == Classes("class 1", "class2")
    assert unordered_list.classes == Classes("class-1", "class2")
    assert unordered_list.tag == "ul"

    # Test with invalid elements
    message = "All elements of UnorderedList must be of type ListItem"
    with pytest.raises(TypeError, match=message):
        UnorderedList(
            elements=Elements(
                ListItem(elements=Elements("First item")),
                "Invalid element",
                ListItem(elements=Elements("Third item")),
            )
        )
