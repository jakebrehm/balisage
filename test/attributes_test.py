"""
Contains tests for the attributes module.
"""

from copy import deepcopy

import pytest

from html_builder.attributes import Attributes, Classes

# TODO: Add edge case tests (invalid class names, data types, etc.)


# MARK: Fixtures


@pytest.fixture
def classes() -> Classes:
    """Creates a sample Classes object."""
    return Classes("class 1", "class2")


@pytest.fixture
def attributes() -> Attributes:
    """Creates a sample Attributes object."""
    return Attributes(
        {
            "class": Classes("class 1", "class2"),
            "id": "test",
            "width": 50,
            "disabled": None,
            "checked": True,
            "itemscope": False,
        }
    )


# MARK: Classes


def test_classes_init(classes: Classes) -> None:
    """Tests the initialization of the Classes class."""
    expected = {"class 1": "class-1", "class2": "class2"}
    assert classes.classes == expected


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


def test_classes_replacements(classes: Classes) -> None:
    """Tests the replacements property of the Classes class."""

    # Test the default replacements
    expected_replacements = {" ": "-"}
    expected_classes = {
        "class 1": "class-1",
        "class2": "class2",
    }
    assert classes.replacements == expected_replacements
    assert classes.classes == expected_classes

    # Try setting new replacements
    new_replacements = {" ": "!", "a": "@"}
    expected_classes = {
        "class 1": "cl@ss!1",
        "class2": "cl@ss2",
    }
    classes.replacements = new_replacements
    assert classes.replacements == new_replacements
    assert classes.classes == expected_classes

    # Try resetting the replacements
    classes.reset_replacements()
    assert classes.replacements == Classes.DEFAULT_REPLACEMENTS


def test_classes_add(classes: Classes) -> None:
    """Tests the add method of the Classes class."""

    # Try adding a single new class that does not exist
    classes.add("Class 3")
    expected = {
        "class 1": "class-1",
        "class2": "class2",
        "Class 3": "class-3",
    }
    assert classes.classes == expected

    # Try adding a single class that already exists pre-sanitation
    classes.add("Class 3")
    expected = {
        "class 1": "class-1",
        "class2": "class2",
        "Class 3": "class-3",
    }
    assert classes.classes == expected

    # Try adding a single class that already exists post-sanitation
    classes.add("class-3")
    expected = {
        "class 1": "class-1",
        "class2": "class2",
        "Class 3": "class-3",
    }
    assert classes.classes == expected

    # Try adding new classes with existing names pre-sanitation
    classes.add("class4", "class 1", "Class 5")
    expected = {
        "class 1": "class-1",
        "class2": "class2",
        "Class 3": "class-3",
        "class4": "class4",
        "Class 5": "class-5",
    }
    assert classes.classes == expected

    # Try adding new classes with existing names post-sanitation
    classes.add("class4", "CLASS-1", "Class 5")
    expected = {
        "class 1": "class-1",
        "class2": "class2",
        "Class 3": "class-3",
        "class4": "class4",
        "Class 5": "class-5",
    }
    assert classes.classes == expected


def test_classes_set(classes: Classes) -> None:
    """Tests the set method of the Classes class."""

    # Try setting classes using a single string
    classes.set("Class 3")
    expected = {"Class 3": "class-3"}
    assert classes.classes == expected

    # Try setting classes using multiple strings
    classes.set("Class 3", "class4", "class--9")
    expected = {
        "Class 3": "class-3",
        "class4": "class4",
        "class--9": "class--9",
    }
    assert classes.classes == expected


def test_classes_remove(classes: Classes) -> None:
    """Tests the remove method of the Classes class."""

    # Try removing a class by its pre-sanitized name
    expected_result = classes.remove("class 1")
    expected_classes = {"class2": "class2"}
    assert expected_result == ("class 1", "class-1")
    assert classes.classes == expected_classes

    # Try removing a class by its post-sanitized name
    expected_result = classes.remove("class2")
    expected_classes = {}
    assert expected_result == ("class2", "class2")
    assert classes.classes == expected_classes

    # Try removing a class that does not exist
    class_to_remove = "cl@ss99"
    message = f"Class '{class_to_remove}' not found"
    with pytest.raises(KeyError, match=message):
        classes.remove(class_to_remove)


def test_classes_clear(classes: Classes) -> None:
    """Tests the clear method of the Classes class."""
    classes.clear()
    assert classes.classes == dict()


def test_classes_sanitize_name(classes: Classes) -> None:
    """Tests the _sanitize_name method of the Classes class."""
    assert classes._sanitize_name("class 1") == "class-1"
    assert classes._sanitize_name("class2") == "class2"
    assert classes._sanitize_name("Class 3") == "class-3"
    assert classes._sanitize_name("  Class   4   ") == "class---4"
    # Test strip and lower options
    test_string = "  ClASs 4 "
    assert classes._sanitize_name(test_string, lower=False) == "ClASs-4"
    assert classes._sanitize_name(test_string, strip=False) == "--class-4-"
    assert (
        classes._sanitize_name(
            test_string,
            lower=False,
            strip=False,
        )
        == "--ClASs-4-"
    )


def test_classes_construct(classes: Classes) -> None:
    """Tests the construct method of the Classes class."""
    assert classes.construct() == "class-1 class2"


def test_classes_eq(classes: Classes) -> None:
    """Tests the __eq__ method of the Classes class."""

    # Try comparing to another Classes object with different keys
    other_classes = Classes("class-1", "class2")
    assert classes == other_classes

    # Try comparing the classes object to other instances of the Classes class
    assert classes == classes
    assert classes == Classes("class 1", "class2")
    assert classes != Classes("class 1", "class3")

    # Try comparing the classes object to near-equivalent dictionaries
    assert classes == {"class 1": "class-1", "class2": "class2"}
    assert classes == {"class-1": "class-1", "class2": "class2"}

    # Try comparing the classes object to other data types
    assert classes != 1
    assert classes != 2.0
    assert classes is not True
    assert classes is not False
    assert classes != tuple()
    assert classes != list()
    assert classes != dict()
    assert classes is not None


def test_classes_bool(classes: Classes) -> None:
    """Tests the __bool__ method of the Classes class."""
    assert bool(classes) is True
    assert bool(Classes()) is False


def test_classes_str(classes: Classes) -> None:
    """Tests the __str__ method of the Classes class."""
    assert str(classes) == "class-1 class2"


def test_classes_repr(classes: Classes) -> None:
    """Tests the __repr__ method of the Classes class."""
    assert repr(classes) == "Classes('class 1', 'class2')"


# MARK: Attributes


def test_attributes_init(attributes: Attributes) -> None:
    """Tests the initialization of the Attributes class."""
    expected = {
        "class": Classes("class 1", "class2"),
        "id": "test",
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
    }
    assert attributes.attributes == expected


def test_attributes_from_string() -> None:
    """Tests the from_string method of the Attributes class."""
    attributes = Attributes.from_string("class='class-1 class2' id='test-1'")
    expected = {"class": Classes("class-1", "class2"), "id": "test-1"}
    assert attributes.attributes == expected


def test_attributes_attributes(attributes: Attributes) -> None:
    """Tests the attributes property of the Attributes class."""
    expected = {
        "class": Classes("class 1", "class2"),
        "id": "test",
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
    }
    assert attributes.attributes == expected


def test_attributes_classes(attributes: Attributes) -> None:
    """Tests the attributes property of the Attributes class."""

    # Test getting classes
    assert attributes.classes == Classes("class 1", "class2")

    # Test setting classes as a string
    expected = "class1"
    attributes.classes = expected
    assert attributes.classes == Classes.from_string(expected)
    expected = "class1 class-2"
    attributes.classes = expected
    assert attributes.classes == Classes.from_string(expected)

    # Test setting classes as a list of strings
    expected = ["class 1", "class2", "Class 3", "cLass4"]
    attributes.classes = expected
    assert attributes.classes == Classes(*expected)

    # Test setting classes as a Classes object
    expected = Classes("class 1", "class2", "Class 3", "cLass4")
    attributes.classes = expected
    assert attributes.classes == expected

    # Test setting classes as other data types
    message = (
        "classes setter accepts either a string, a list of strings, or an "
        "instance of Attributes"
    )
    for invalid_value in [True, False, None, 1, 2.0, tuple(), list(), dict()]:
        with pytest.raises(TypeError, match=message):
            attributes.classes = invalid_value


def test_attributes_add(attributes: Attributes) -> None:
    """Tests the add method of the Attributes class."""

    # Try adding a single new attribute that does not exist
    attributes.add({"required": True})
    expected = {
        "class": Classes("class 1", "class2"),
        "id": "test",
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
        "required": True,
    }
    assert attributes.attributes == expected

    # Try adding a single attribute that already exists
    attributes.add({"checked": False})
    expected = {
        "class": Classes("class 1", "class2"),
        "id": "test",
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
        "required": True,
    }
    assert attributes.attributes == expected

    # Try adding multiple new attributes that already exist
    attributes.add({"itemscope": None, "disabled": None})
    expected = {
        "class": Classes("class 1", "class2"),
        "id": "test",
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
        "required": True,
    }
    assert attributes.attributes == expected

    # Try adding multiple new attributes that do not exist
    attributes.add({"height": 50, "open": True, "alt": "Alternate text"})
    expected = {
        "class": Classes("class 1", "class2"),
        "id": "test",
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
        "required": True,
        "height": 50,
        "open": True,
        "alt": "Alternate text",
    }
    assert attributes.attributes == expected

    # Try adding a mix of new and existing attributes
    attributes.add({"checked": False, "title": "Title text"})
    expected = {
        "class": Classes("class 1", "class2"),
        "id": "test",
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
        "required": True,
        "height": 50,
        "open": True,
        "alt": "Alternate text",
        "title": "Title text",
    }
    assert attributes.attributes == expected


def test_attributes_set(attributes: Attributes) -> None:
    """Tests the set method of the Attributes class."""
    expected = {
        "class": Classes("class 1", "class2"),
        "id": "test",
        "width": 75,
        "disabled": None,
        "checked": True,
        "itemscope": False,
        "alt": "Attributes test",
    }
    attributes.set(expected)
    assert attributes.attributes == expected
    attributes.set(expected)
    assert attributes.attributes == expected


def test_attributes_remove(attributes: Attributes) -> None:
    """Tests the remove method of the Attributes class."""

    # Try removing an attribute by its name
    expected_result = attributes.remove("id")
    expected_attributes = {
        "class": Classes("class 1", "class2"),
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
    }
    assert expected_result == ("id", "test")
    assert attributes.attributes == expected_attributes

    # Try removing an attribute that does not exist
    attribute_to_remove = "does-not-exist"
    message = f"Attribute '{attribute_to_remove}' not found"
    with pytest.raises(KeyError, match=message):
        attributes.remove(attribute_to_remove)


def test_attributes_clear(attributes: Attributes) -> None:
    """Tests the clear method of the Attributes class."""
    attributes.clear()
    assert attributes.attributes == dict()


def test_attributes_construct(attributes: Attributes) -> None:
    """Tests the construct method of the Attributes class."""
    assert attributes.construct() == (
        "class='class-1 class2' id='test' width='50' disabled checked"
    )


def test_attributes_get_set(attributes: Attributes) -> None:
    """Tests the __getitem__ and __setitem__ methods of the Attributes class."""

    # Verify that the attributes have not yet been changed
    assert attributes["class"] != Classes("class-1", "class2", "class3")
    assert attributes["id"] != "test-1"
    assert attributes["width"] != 100
    assert attributes["disabled"] is not True
    assert attributes["checked"] is not None
    assert attributes["itemscope"] is not None
    assert "required" not in attributes.attributes

    # Change the attributes
    attributes["class"] = Classes("class-1", "class2", "class3")
    attributes["id"] = "test-1"
    attributes["width"] = 100
    attributes["disabled"] = True
    attributes["checked"] = None
    attributes["itemscope"] = True
    attributes["required"] = True

    # Verify that the attributes have been changed
    assert attributes["class"] == Classes("class-1", "class2", "class3")
    assert attributes["id"] == "test-1"
    assert attributes["width"] == 100
    assert attributes["disabled"] is True
    assert attributes["checked"] is None
    assert attributes["itemscope"] is True
    assert attributes["required"] is True


def test_attributes_eq(attributes: Attributes) -> None:
    """Tests the __eq__ method of the Attributes class."""

    # Try comparing the attributes object to itself
    assert attributes == attributes

    # Try comparing the attributes object to one with the same values
    expected = Attributes(
        {
            "class": Classes("class 1", "class2"),
            "id": "test",
            "width": 50,
            "disabled": None,
            "checked": True,
            "itemscope": False,
        }
    )
    assert attributes == expected

    # Try comparing the attributes object to itself with values changed
    expected = deepcopy(attributes)
    expected.add({"required": True})
    assert attributes != expected

    # Try comparing the attributes object to one with different values
    expected = Attributes(
        {
            "class": Classes("class 1", "class2", "class3"),
            "id": "test-1",
            "width": 50,
            "disabled": False,
            "checked": True,
            "itemscope": None,
            "required": True,
        }
    )
    assert attributes != expected

    # Try comparing the attributes object to dictionaries
    expected = {
        "class": Classes("class 1", "class2"),
        "id": "test",
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
    }
    assert attributes == expected

    # Try comparing the attributes object to other data types
    assert attributes != 1
    assert attributes != 2.0
    assert attributes is not True
    assert attributes is not False
    assert attributes != tuple()
    assert attributes != list()
    assert attributes != dict()
    assert attributes is not None


def test_attributes_bool(attributes: Attributes) -> None:
    """Tests the __bool__ method of the Attributes class."""
    assert bool(attributes) is True
    assert bool(Attributes()) is False


def test_attributes_str(attributes: Attributes) -> None:
    """Tests the __str__ method of the Attributes class."""
    expected = "class='class-1 class2' id='test' width='50' disabled checked"
    assert str(attributes) == expected


def test_attributes_repr(attributes: Attributes) -> None:  # TODO: Fix
    """Tests the __repr__ method of the Attributes class."""
    expected = (
        "Attributes(attributes={"
        "'class': Classes('class 1', 'class2'), "
        "'id': 'test', "
        "'width': 50, "
        "'disabled': None, "
        "'checked': True, "
        "'itemscope': False"
        "})"
    )
    assert repr(attributes) == expected
