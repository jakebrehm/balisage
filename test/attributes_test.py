"""
Contains tests for the attributes module.
"""

from collections import OrderedDict

import pytest

from html_builder.attributes import Classes


@pytest.fixture
def classes() -> Classes:
    """Creates a sample Classes object."""
    return Classes("class 1", "class2")


def test_classes_init(classes: Classes) -> None:
    """Tests the initialization of the Classes class."""
    assert classes.classes == {"class 1": "class-1", "class2": "class2"}


def test_classes_from_string() -> None:
    """Tests the from_string method of the Classes class."""
    classes = Classes.from_string("class1 class2 Class-3 cLass4")
    expected = {
        "class1": "class1",
        "class2": "class2",
        "Class-3": "class-3",
        "cLass4": "class4",
    }
    assert classes.classes == expected
    assert classes.classes == OrderedDict(expected)


def test_classes_replacements(classes: Classes) -> None:
    """Tests the replacements property of the Classes class."""

    # Test the default replacements
    expected_replacements = {" ": "-"}
    expected_classes = {
        "class 1": "class-1",
        "class2": "class2",
    }
    assert classes.replacements == OrderedDict(expected_replacements)
    assert classes.classes == OrderedDict(expected_classes)

    # Try setting new replacements
    new_replacements = {" ": "!", "a": "@"}
    expected_classes = {
        "class 1": "cl@ss!1",
        "class2": "cl@ss2",
    }
    classes.replacements = new_replacements
    assert classes.replacements == OrderedDict(new_replacements)
    assert classes.classes == OrderedDict(expected_classes)

    # Try resetting the replacements
    classes.reset_replacements()
    assert classes.replacements == Classes.DEFAULT_REPLACEMENTS


def test_classes_add(classes: Classes) -> None:  # TODO: Implement
    """Tests the add method of the Classes class."""

    # Try adding a single new class
    classes.add("Class 3")
    expected = {
        "class 1": "class-1",
        "class2": "class2",
        "Class 3": "class-3",
    }
    assert classes.classes == OrderedDict(expected)

    # Try adding a single class that already exists pre-sanitation
    classes.add("Class 3")
    expected = {
        "class 1": "class-1",
        "class2": "class2",
        "Class 3": "class-3",
    }
    assert classes.classes == OrderedDict(expected)

    # Try adding a single class that already exists post-sanitation
    classes.add("class-3")
    expected = {
        "class 1": "class-1",
        "class2": "class2",
        "Class 3": "class-3",
    }
    assert classes.classes == OrderedDict(expected)

    # Try adding new classes with existing names pre-sanitation
    classes.add("class4", "class 1", "Class 5")
    expected = {
        "class 1": "class-1",
        "class2": "class2",
        "Class 3": "class-3",
        "class4": "class4",
        "Class 5": "class-5",
    }
    assert classes.classes == OrderedDict(expected)

    # Try adding new classes with existing names post-sanitation
    classes.add("class4", "CLASS-1", "Class 5")
    expected = {
        "class 1": "class-1",
        "class2": "class2",
        "Class 3": "class-3",
        "class4": "class4",
        "Class 5": "class-5",
    }
    assert classes.classes == OrderedDict(expected)


def test_classes_set(classes: Classes) -> None:
    """Tests the set method of the Classes class."""
    classes.set("Class 3", "class4", "class--9")
    expected = {
        "Class 3": "class-3",
        "class4": "class4",
        "class--9": "class--9",
    }
    assert classes.classes == OrderedDict(expected)


def test_classes_remove(classes: Classes) -> None:
    """Tests the remove method of the Classes class."""

    # Try removing a class by its pre-sanitized name
    expected_result = classes.remove("class 1")
    expected_classes = {"class2": "class2"}
    assert expected_result == ("class 1", "class-1")
    assert classes.classes == expected_classes
    assert classes.classes == OrderedDict(expected_classes)

    # Try removing a class by its post-sanitized name
    expected_result = classes.remove("class2")
    expected_classes = {}
    assert expected_result == ("class2", "class2")
    assert classes.classes == OrderedDict(expected_classes)

    # Try removing a class that does not exist
    with pytest.raises(KeyError):
        classes.remove("cl@ss99")


def test_classes_clear(classes: Classes) -> None:
    """Tests the clear method of the Classes class."""
    classes.clear()
    assert classes.classes == OrderedDict()


def test_classes_sanitize_name(classes: Classes) -> None:
    """Tests the _sanitize_name method of the Classes class."""
    assert classes._sanitize_name("class 1") == "class-1"
    assert classes._sanitize_name("class2") == "class2"
    assert classes._sanitize_name("Class 3") == "class-3"
    assert classes._sanitize_name("  Class   4   ") == "class---4"


def test_classes_construct(classes: Classes) -> None:
    """Tests the construct method of the Classes class."""
    assert classes.construct() == "class-1 class2"


def test_classes_str(classes: Classes) -> None:
    """Tests the __str__ method of the Classes class."""
    assert str(classes) == "class='class-1 class2'"


def test_classes_repr(classes: Classes) -> None:
    """Tests the __repr__ method of the Classes class."""
    assert repr(classes) == "Classes('class 1', 'class2')"
