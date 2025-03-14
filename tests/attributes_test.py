"""
Contains tests for the attributes module.
"""

import re
from copy import deepcopy

import pytest

from balisage.attributes import Attributes, Classes, Elements
from balisage.elements.format import HorizontalRule, LineBreak
from balisage.elements.image import Image
from balisage.elements.styles import Div
from balisage.types import Element

# MARK: Fixtures


@pytest.fixture
def classes() -> Classes:
    """Creates a sample Classes object."""
    return Classes("class 1", "clAss2")


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


@pytest.fixture
def element_data() -> list[Element]:
    """Creates a sample list of data."""
    return [
        Div(
            elements=Elements(
                HorizontalRule(),
                Image(
                    attributes=Attributes({"src": "image.png"}),
                ),
            )
        ),
        LineBreak(),
    ]


@pytest.fixture
def elements(element_data: list[Element]) -> Elements:
    """Creates a sample Elements object that has elements."""
    return Elements(*element_data)


# MARK: Classes


def test_classes_init(classes: Classes) -> None:
    """Tests the initialization of the Classes class."""
    assert classes.classes == {"class 1": "class-1", "clAss2": "class2"}


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
        "clAss2": "class2",
    }
    assert classes.replacements == expected_replacements
    assert classes.classes == expected_classes

    # Try setting new replacements
    new_replacements = {" ": "_", "a": "zz"}
    expected_classes = {
        "class 1": "clzzss_1",
        "clAss2": "clzzss2",
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
        "clAss2": "class2",
        "Class 3": "class-3",
    }
    assert classes.classes == expected

    # Try adding a single class that already exists pre-sanitation
    classes.add("Class 3")
    expected = {
        "class 1": "class-1",
        "clAss2": "class2",
        "Class 3": "class-3",
    }
    assert classes.classes == expected

    # Try adding a single class that already exists post-sanitation
    classes.add("class-3")
    expected = {
        "class 1": "class-1",
        "clAss2": "class2",
        "Class 3": "class-3",
    }
    assert classes.classes == expected

    # Try adding new classes with existing names pre-sanitation
    classes.add("class4", "class 1", "Class 5")
    expected = {
        "class 1": "class-1",
        "clAss2": "class2",
        "Class 3": "class-3",
        "class4": "class4",
        "Class 5": "class-5",
    }
    assert classes.classes == expected

    # Try adding new classes with existing names post-sanitation
    classes.add("class4", "CLASS-1", "Class 5")
    expected = {
        "class 1": "class-1",
        "clAss2": "class2",
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

    # Try settings with no arguments
    classes.set()
    assert classes.classes == {}

    # Try setting with a mix of strings and non-strings
    message = "Arguments passed to set must be strings"
    with pytest.raises(TypeError, match=message):
        classes.set("Class 3", 1, 2.0, True, None, tuple(), list(), dict())

    # Try setting with only non-strings
    with pytest.raises(TypeError, match=message):
        classes.set(1, 2.0, True, None, tuple(), list(), dict())


def test_classes_remove(classes: Classes) -> None:
    """Tests the remove method of the Classes class."""

    # Try removing a class by its pre-sanitized name
    expected_result = classes.remove("class 1")
    expected_classes = {"clAss2": "class2"}
    assert expected_result == ("class 1", "class-1")
    assert classes.classes == expected_classes

    # Try removing a class by its post-sanitized name
    expected_result = classes.remove("class2")
    expected_classes = {}
    assert expected_result == ("clAss2", "class2")
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
    assert classes._sanitize_name("clAss2") == "class2"
    assert classes._sanitize_name("Class 3") == "class-3"
    assert classes._sanitize_name("  Class   4   ") == "class---4"


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
    assert repr(classes) == "Classes('class 1', 'clAss2')"


# MARK: Attributes


def test_attributes_init(attributes: Attributes) -> None:
    """Tests the initialization of the Attributes class."""
    expected_classes = Classes("class 1", "class2")
    expected_attributes = {
        "class": expected_classes,
        "id": "test",
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
    }
    assert attributes.attributes == expected_attributes
    assert attributes.classes == expected_classes


def test_attributes_from_string() -> None:
    """Tests the from_string method of the Attributes class."""
    string = "class='class-1 class2' id='test-1' disabled"
    attributes = Attributes.from_string(string)
    expected = {
        "class": Classes("class-1", "class2"),
        "id": "test-1",
        "disabled": True,
    }
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

    # Test setting classes as a string
    expected = {"class1": "class1"}
    attributes.classes = "class1"
    assert attributes.classes == Classes(*expected.keys())
    assert attributes.classes.classes == expected
    expected = {"class1": "class1", "class-2": "class-2"}
    attributes.classes = "class1 class-2"
    assert attributes.classes == Classes(*expected.keys())
    assert attributes.classes.classes == expected

    # Test setting classes as a Classes object
    expected = {
        "class 1": "class-1",
        "class2": "class2",
        "Class 3": "class-3",
        "cLass4": "class4",
    }
    attributes.classes = Classes("class 1", "class2", "Class 3", "cLass4")
    assert attributes.classes == expected
    assert attributes.classes.classes == expected

    # Test setting classes as a list of strings
    invalid_value = ["class 1", "class2", "Class 3", "cLass4"]
    message = "Arguments passed to set must be strings"
    with pytest.raises(TypeError, match=message):
        attributes.classes = invalid_value

    # Test setting classes as other data types
    for invalid_value in [True, False, None, 1, 2.0, tuple(), list(), dict()]:
        with pytest.raises(TypeError, match=message):
            attributes.classes = invalid_value

    # Test with a default instance
    attributes = Attributes()
    assert attributes.classes == Classes()


def test_attributes_add(attributes: Attributes) -> None:
    """Tests the add method of the Attributes class."""

    expected_classes = Classes("class 1", "class2")

    # Try adding a single new attribute that does not exist
    attributes.add({"required": True})
    expected_attributes = {
        "class": expected_classes,
        "id": "test",
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
        "required": True,
    }
    assert attributes.attributes == expected_attributes

    # Try adding a single attribute that already exists
    attributes.add({"checked": False})
    expected_attributes = {
        "class": expected_classes,
        "id": "test",
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
        "required": True,
    }
    assert attributes.attributes == expected_attributes

    # Try adding multiple new attributes that already exist
    attributes.add({"itemscope": None, "disabled": None})
    expected_attributes = {
        "class": expected_classes,
        "id": "test",
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
        "required": True,
    }
    assert attributes.attributes == expected_attributes

    # Try adding multiple new attributes that do not exist
    attributes.add({"height": 50, "open": True, "alt": "Alternate text"})
    expected_attributes = {
        "class": expected_classes,
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
    assert attributes.attributes == expected_attributes

    # Try adding a mix of new and existing attributes
    attributes.add({"checked": False, "title": "Title text"})
    expected_attributes = {
        "class": expected_classes,
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
    assert attributes.attributes == expected_attributes

    # Try adding a string to a fresh instance
    attributes = Attributes()
    assert attributes == Attributes()
    assert attributes.attributes == {"class": Classes()}
    attributes.add({"class": "class-3"})
    assert attributes.attributes == {"class": Classes()}
    assert attributes.attributes != {"class": Classes("class-3")}

    # Try adding a Classes object to a fresh instance
    attributes = Attributes()
    assert attributes == Attributes()
    assert attributes.attributes == {"class": Classes()}
    attributes.add({"class": Classes("class-3")})
    assert attributes.attributes == {"class": Classes()}
    assert attributes.attributes != {"class": Classes("class-3")}


def test_attributes_set(attributes: Attributes) -> None:
    """Tests the set method of the Attributes class."""

    # Test with classes passes as a string
    expected = {
        "class": "class-1 class2",
        "id": "test",
        "width": 75,
        "disabled": None,
        "checked": True,
        "itemscope": False,
        "alt": "Attributes test",
    }
    attributes.set(expected)
    assert attributes.attributes == expected

    # Test with classes passes as a Classes object
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

    # Set to attributes with no classes
    attributes = Attributes()
    attributes.set({})
    assert attributes.attributes == {"class": Classes()}
    attributes.set({"class": None})
    assert attributes.attributes == {"class": Classes()}


def test_attributes_remove(attributes: Attributes) -> None:
    """Tests the remove method of the Attributes class."""

    # Try removing an attribute by its name
    expected_classes = Classes("class 1", "class2")
    expected_attributes = {
        "class": expected_classes,
        "width": 50,
        "disabled": None,
        "checked": True,
        "itemscope": False,
    }
    attributes.remove("id")
    assert attributes.attributes == expected_attributes
    assert attributes.classes == expected_classes

    # Try removing the class attributes
    attributes.remove("class")
    expected_attributes["class"] = Classes()
    assert attributes.attributes == expected_attributes
    assert attributes.classes == Classes()

    # Try removing an attribute that does not exist
    attribute_to_remove = "does-not-exist"
    message = f"Attribute '{attribute_to_remove}' not found"
    with pytest.raises(KeyError, match=message):
        attributes.remove(attribute_to_remove)


def test_attributes_clear(attributes: Attributes) -> None:
    """Tests the clear method of the Attributes class."""
    attributes.clear()
    assert attributes == Attributes()
    assert attributes.attributes == {"class": Classes()}
    assert attributes.classes == Classes()


def test_attributes_construct(attributes: Attributes) -> None:
    """Tests the construct method of the Attributes class."""
    assert attributes.construct() == (
        "class='class-1 class2' id='test' width='50' disabled checked"
    )
    assert Attributes().construct() == ""


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

    # Test with a fresh instance
    attributes = Attributes()
    assert attributes["class"] == Classes()
    with pytest.raises(KeyError):
        attributes["id"]


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

    # Try comparing the attributes object to a dictionary
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
    # Try with an Attributes instance that has no classes
    attributes = Attributes(
        {
            "id": "test",
            "disabled": True,
            "class": Classes(),
        }
    )
    assert bool(attributes) is True


def test_attributes_str(attributes: Attributes) -> None:
    """Tests the __str__ method of the Attributes class."""
    expected = "class='class-1 class2' id='test' width='50' disabled checked"
    assert str(attributes) == expected


def test_attributes_repr(attributes: Attributes) -> None:
    """Tests the __repr__ method of the Attributes class."""

    # Test using the fixture
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

    # Test with no attributes
    attributes = Attributes()
    assert repr(attributes) == "Attributes()"


# MARK: Elements


def test_elements_init(
    elements: Elements, element_data: list[Element]
) -> None:
    """Tests the initialization of the Elements class."""

    # Test with only builder elements
    expected = element_data
    assert elements.elements == expected

    # Test with only one string
    expected = "String 1"
    elements = Elements(expected)
    assert elements.elements == [expected]

    # Test with multiple strings
    expected = ["String 1", "String 2"]
    elements = Elements(*expected)
    assert elements.elements == expected

    # Test with both builder and string elements
    expected = ["String 1", HorizontalRule()]
    elements = Elements(*expected)
    assert elements.elements == expected

    # Test with invalid data types
    invalid_values = [1, 2.0, True, False, tuple(), dict(), None]
    message = "Elements must be strings or builder objects"
    for invalid_value in invalid_values:
        with pytest.raises(TypeError, match=message):
            Elements(invalid_value)


def test_elements_max_elements(elements: Elements) -> None:
    """Tests the max_elements property of the Elements class."""

    # Test the default max_elements and setting to valid values
    assert elements.max_elements is None
    for test_value in [10, None]:
        elements.max_elements = test_value
        assert elements.max_elements == test_value

    # Verify that a new instance's max elements is None
    assert Elements().max_elements is None

    # Set max elements to a value that is not an int or None
    message = "max_elements must be an int or None"
    test_values = ["10", 10.0, True, False, tuple(), list(), dict()]
    for test_value in test_values:
        with pytest.raises(TypeError, match=message):
            elements.max_elements = test_value

    # Set max elements to a negative value
    message = "max_elements must be a positive integer"
    with pytest.raises(ValueError, match=message):
        elements.max_elements = -1

    # Set max elements to a value equal to the current number of elements
    elements.max_elements = 2

    # Set max elements to a value less than the current number of elements
    message = (
        "max_elements must be greater than or equal to the current "
        "number of elements (2)"
    )
    with pytest.raises(ValueError, match=re.escape(message)):
        elements.max_elements = 1


def test_elements_valid_types(elements: Elements) -> None:
    """Tests the valid_types property of the Elements class."""

    # Try setting valid_types to types incompatible with the current elements
    message = "Types of current elements are not one of (int,)"
    with pytest.raises(TypeError, match=re.escape(message)):
        elements.valid_types = int

    # Test the default valid_types and clear the elements
    elements.clear()
    assert elements.valid_types is None

    # Set valid_types to something valid
    for test_value, expected_value in [
        (int, (int,)),
        ([int], (int,)),
        ((int,), (int,)),
        ([int, str], (int, str)),
        ((int, str), (int, str)),
    ]:
        elements.valid_types = test_value
        assert elements.valid_types == expected_value

    # Set valid_types to None again
    elements.valid_types = None
    assert elements.valid_types is None

    # Set valid_types to empty lists and tuples
    for test_value in [tuple(), list()]:
        elements.valid_types = test_value
        assert elements.valid_types is None

    # Set valid_types to an invalid value
    message = "Expected a type, got instance of int"
    with pytest.raises(TypeError, match=re.escape(message)):
        elements.valid_types = 1


def test_elements_add(elements: Elements, element_data: list[Element]) -> None:
    """Tests the add method of the Elements class."""

    # Try adding a single new element
    new_element = HorizontalRule()
    elements.add(new_element)
    expected_elements = element_data + [new_element]
    assert elements.elements == expected_elements

    # Try adding multiple new elements
    new_elements = [LineBreak(), HorizontalRule()]
    elements.add(*new_elements)
    expected_elements = expected_elements + new_elements
    assert elements.elements == expected_elements

    # Try adding new elements that are allowed
    elements.clear()
    elements.valid_types = str
    new_element = "Test string"
    elements.add(new_element)
    assert elements.elements == [new_element]

    # Try adding new elements that are not allowed
    message = "Got LineBreak, expected one of (str,)"
    with pytest.raises(TypeError, match=re.escape(message)):
        elements.add(LineBreak())


def test_elements_set(elements: Elements) -> None:
    """Tests the set method of the Elements class."""

    # Try setting a single builder element
    new_data = HorizontalRule()
    elements.set(new_data)
    assert elements.elements == [new_data]

    # Try setting multiple builder elements
    new_data = [LineBreak(), HorizontalRule()]
    elements.set(*new_data)
    assert elements.elements == new_data

    # Try setting a single string element
    new_data = "Test string"
    elements.set(new_data)
    assert elements.elements == [new_data]

    # Try setting multiple string elements
    new_data = ["Test string 1", "Test string 2"]
    elements.set(*new_data)
    assert elements.elements == new_data

    # Try setting a mix of builder and string elements
    new_data = [LineBreak(), "Test string", HorizontalRule()]
    elements.set(*new_data)
    assert elements.elements == new_data

    # Try setting new elements that are allowed
    elements.clear()
    elements.valid_types = str
    new_data = "Test string"
    elements.set(new_data)
    assert elements.elements == [new_data]

    # Try setting new elements that are not allowed
    message = "Got LineBreak, expected one of (str,)"
    with pytest.raises(TypeError, match=re.escape(message)):
        elements.set(LineBreak())


def test_elements_insert(
    elements: Elements, element_data: list[Element]
) -> None:
    """Tests the insert method of the Elements class."""
    new_element = HorizontalRule()
    element_data.insert(1, new_element)
    elements.insert(1, new_element)
    assert elements.elements == element_data

    # Try inserting elements that are allowed
    elements.clear()
    elements.valid_types = str
    expected_data = ["Test string 1", "Test string 2"]
    elements.add(*expected_data)
    new_data = "Test string"
    expected_data.insert(1, new_data)
    elements.insert(1, new_data)
    assert elements.elements == expected_data

    # Try inserting elements that are not allowed
    message = "Got LineBreak, expected one of (str,)"
    with pytest.raises(TypeError, match=re.escape(message)):
        elements.insert(1, LineBreak())


def test_elements_update(
    elements: Elements, element_data: list[Element]
) -> None:
    """Tests the update method of the Elements class."""
    new_element = HorizontalRule()
    expected_data = element_data
    expected_data[0] = new_element
    elements.update(0, new_element)
    assert elements.elements[0] == new_element
    assert elements.elements == expected_data
    assert len(elements.elements) == 2

    # Try updating with elements that are allowed
    elements.clear()
    elements.valid_types = str
    expected_data = ["Test string 1", "Test string 2"]
    elements.add(*expected_data)
    new_element = "Test string"
    expected_data[0] = new_element
    elements.update(0, new_element)
    assert elements.elements[0] == new_element
    assert elements.elements == expected_data
    assert len(elements.elements) == 2

    # Try updating with elements that are not allowed
    message = "Got HorizontalRule, expected one of (str,)"
    with pytest.raises(TypeError, match=re.escape(message)):
        elements.update(0, HorizontalRule())


def test_elements_remove(
    elements: Elements, element_data: list[Element]
) -> None:
    """Tests the remove and __delitem__ methods of the Elements class."""

    # Test the remove method
    elements.remove(-1)
    assert elements.elements == element_data[:-1]
    assert len(elements.elements) == (len(element_data) - 1)

    # Test the __delitem__ method
    del elements[-1]
    assert elements.elements == []
    assert len(elements.elements) == 0


def test_elements_pop(elements: Elements, element_data: list[Element]) -> None:
    """Tests the pop method of the Elements class."""

    # Pop with an integer argument
    popped_element = elements.pop(0)
    assert popped_element == element_data[0]
    assert elements.elements == element_data[1:]
    assert len(elements.elements) == (len(element_data) - 1)

    # Pop with a non-integer argument
    with pytest.raises(TypeError):
        elements.pop("1")

    # Pop with no arguments
    popped_element = elements.pop()
    assert popped_element == element_data[-1]
    assert elements.elements == []
    assert len(elements.elements) == (len(element_data) - 2)


def test_elements_clear(elements: Elements) -> None:
    """Tests the clear method of the Elements class."""
    elements.clear()
    assert elements.elements == []
    assert len(elements.elements) == 0


def test_elements_raise_if_exceeds_max_elements(elements: Elements) -> None:
    """Tests the _raise_if_exceeds_max_elements method of the Elements class."""

    # Try adding a new element to exceed max_elements
    elements.max_elements = 2
    message = "3 elements would exceed the maximum number of elements (2)"
    with pytest.raises(ValueError, match=re.escape(message)):
        elements.add(LineBreak())

    # Try inserting a new element to exceed max_elements
    message = "3 elements would exceed the maximum number of elements (2)"
    with pytest.raises(ValueError, match=re.escape(message)):
        elements.insert(0, LineBreak())

    # Try setting new elements to exceed max_elements
    message = "3 elements would exceed the maximum number of elements (2)"
    with pytest.raises(ValueError, match=re.escape(message)):
        elements.set(LineBreak(), HorizontalRule(), Div())

    # Test different versions of pluralization in the error message
    elements.clear()
    elements.max_elements = 0
    message = "1 element would exceed the maximum number of elements (0)"
    with pytest.raises(ValueError, match=re.escape(message)):
        elements.add(LineBreak())


def test_elements_get_set(
    elements: Elements, element_data: list[Element]
) -> None:
    """Tests the __getitem__ and __setitem__ methods of the Elements class."""
    new_element = HorizontalRule()
    expected_data = element_data
    expected_data[0] = new_element
    elements[0] = new_element
    assert elements[0] == new_element
    assert elements.elements == expected_data
    assert len(elements.elements) == 2


def test_elements_iter(
    elements: Elements, element_data: list[Element]
) -> None:
    """Tests the __iter__ method of the Elements class."""

    # Test with builder elements
    for actual_element, expected_element in zip(elements, element_data):
        assert actual_element == expected_element

    # Test with strings
    element_data = ["String 1", "String 2"]
    elements = Elements(*element_data)
    for actual_element, expected_element in zip(elements, element_data):
        assert actual_element == expected_element

    # Test with mixed elements
    element_data = ["String 1", HorizontalRule()]
    elements = Elements(*element_data)
    for actual_element, expected_element in zip(elements, element_data):
        assert actual_element == expected_element


def test_elements_eq(elements: Elements, element_data: list[Element]) -> None:
    """Tests the __eq__ method of the Elements class."""

    # Try comparing the elements object to itself
    assert elements == elements

    # Try comparing the elements object to one with the same values
    expected = Elements(*element_data)
    assert elements == expected

    # Try comparing the elements object to itself with values changed
    expected = deepcopy(elements)
    expected.add(HorizontalRule())
    assert elements != expected

    # Try comparing the elements object to one with different values
    expected = Elements(HorizontalRule(), LineBreak())
    assert elements != expected

    # Try comparing the elements object to one with only strings
    expected = Elements("Test string 1", "Test string 2")
    assert elements != expected

    # Try comparing the elements object to one with strings and elements
    expected = Elements("Test string 1", LineBreak())
    assert elements != expected
    assert Elements("Test string", LineBreak()) == ["Test string", LineBreak()]

    # Try comparing the elements object to a list of strings and elements
    expected = ["Test string 1", LineBreak()]
    assert elements != expected

    # Try comparing the elements object to a list of elements
    assert elements == element_data

    # Try comparing the elements object to other data types
    assert elements != "Test string"
    assert elements != 1
    assert elements != 2.0
    assert elements is not True
    assert elements is not False
    assert elements != tuple()
    assert elements != list()
    assert elements != dict()
    assert elements is not None


def test_elements_bool(elements: Elements) -> None:
    """Tests the __bool__ method of the Elements class."""
    assert bool(elements) is True
    assert bool(Elements()) is False


def test_elements_len(elements: Elements) -> None:
    """Tests the __len__ method of the Elements class."""
    assert len(elements) == len(elements.elements)
    assert len(elements) == 2
    assert len(elements) != 3
    assert len(elements) != 1.0
    assert len(elements) != list()
    assert len(elements) != tuple()
    assert len(elements) != dict()
    assert len(elements) is not True
    assert len(elements) is not False
    assert len(elements) is not None


def test_elements_str(elements: Elements) -> None:
    """Tests the __str__ method of the Elements class."""

    # Try using the fixture
    assert str(elements) == "<div><hr><img src='image.png'></div><br>"

    # Try using elements with mixed types
    elements = Elements(Div(), LineBreak(), "Test string", HorizontalRule())
    assert str(elements) == "<div></div><br>Test string<hr>"

    # Try with some elements that have attributes
    elements = Elements(
        Div(attributes=Attributes({"id": "test"})),
        "Test string",
        HorizontalRule(),
    )
    assert str(elements) == ("<div id='test'></div>Test string<hr>")


def test_elements_repr(elements: Elements) -> None:
    """Tests the __repr__ method of the Elements class."""

    # Try using the fixture
    expected = "Elements(Div(), LineBreak())"
    assert repr(elements) == expected

    # Try using elements with mixed types
    elements = Elements(Div(), LineBreak(), "Test string", HorizontalRule())
    assert repr(elements) == (
        "Elements(Div(), LineBreak(), 'Test string', HorizontalRule())"
    )

    # Try with some elements that have attributes
    elements = Elements(
        Div(attributes=Attributes({"id": "test"})),
        "Test string",
        HorizontalRule(),
    )
    assert repr(elements) == (
        "Elements(Div("
        "attributes=Attributes(attributes={'id': 'test', 'class': Classes()})), "
        "'Test string', "
        "HorizontalRule()"
        ")"
    )
