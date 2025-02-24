"""
Contains tests for the elements.tables module.
"""

import pandas as pd
import pytest

from html_builder.attributes import Attributes, Classes, Elements
from html_builder.elements.tables import Data, Header, Row, Table

# TODO: Test mismatched row lengths, etc.

# MARK: Fixtures


@pytest.fixture
def sample_attributes() -> Attributes:
    """Creates a sample Attributes object."""
    return Attributes({"id": "test", "disabled": True})


@pytest.fixture
def sample_classes() -> Classes:
    """Creates a sample Classes object."""
    return Classes("class 1", "class2")


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Creates a sample pandas dataframe."""
    return pd.DataFrame(
        {
            "A": [1, 2, 3],
            "B": [4, 5, 6],
            "C": [7, 8, 9],
        }
    )


@pytest.fixture
def data(
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> Data:
    """Creates a sample Data object that has classes and attributes."""
    return Data(
        data="Test data",
        attributes=sample_attributes,
        classes=sample_classes,
    )


@pytest.fixture
def row(
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> Row:
    """Creates a sample Row object that has classes and attributes."""
    return Row(
        data=[Data("Test data 1"), Data("Test data 2")],
        attributes=sample_attributes,
        classes=sample_classes,
    )


@pytest.fixture
def header(
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> Header:
    """Creates a sample Header object that has classes and attributes."""
    return Header(
        data=[Data("Test data 1"), Data("Test data 2")],
        attributes=sample_attributes,
        classes=sample_classes,
    )


@pytest.fixture
def table(
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> Table:
    """Creates a sample Table object that has classes and attributes."""
    return Table(
        rows=[
            Row([Data("Test data 1"), Data("Test data 2")]),
            Row([Data("Test data 3"), Data("Test data 4")]),
        ],
        header=Header([Data("Column 1"), Data("Column 2")]),
        attributes=sample_attributes,
        classes=sample_classes,
    )


# MARK: Data


def test_data_init(
    data: Data,
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> None:
    """Tests the initialization of the Data class."""

    # Test with arguments from fixture
    assert data == data
    assert data.attributes == sample_attributes
    assert data.classes == sample_classes
    assert data.classes == Classes("class-1", "class2")
    assert data.data == "Test data"
    assert data.elements.max_elements == 1
    assert data.tag == "td"
    assert data.is_header is False

    # Test with default arguments
    data = Data()
    assert data == data
    assert data.attributes == Attributes()
    assert data.classes == Classes()
    assert data.data is None
    assert data.elements.max_elements == 1
    assert data.tag == "td"
    assert data.is_header is False

    # Test as header data
    data = Data(
        data="Test data",
        attributes=sample_attributes,
        classes=sample_classes,
        is_header=True,
    )
    assert data == data
    assert data.attributes == sample_attributes
    assert data.classes == sample_classes
    assert data.classes == Classes("class-1", "class2")
    assert data.data == "Test data"
    assert data.elements.max_elements == 1
    assert data.tag == "th"
    assert data.is_header is True


def test_data_data(data: Data) -> None:
    """Tests the data property of the Data class."""
    assert data.data == "Test data"


def test_data_set(data: Data) -> None:
    """Tests the set method of the Data class."""
    data.set("New data")
    assert data.data == "New data"


def test_data_clear(data: Data) -> None:
    """Tests the clear method of the Data class."""
    data.clear()
    assert data.data is None


def test_data_is_header(data: Data) -> None:
    """Tests the is_header property of the Data class."""
    assert data.is_header is False
    assert data.tag == "td"
    data.is_header = True
    assert data.is_header is True
    assert data.tag == "th"
    data.is_header = False
    assert data.is_header is False
    assert data.tag == "td"


def test_data_construct(data: Data) -> None:
    """Tests the construct method of the Data class."""
    expected = "<td id='test' disabled class='class-1 class2'>Test data</td>"
    assert data.construct() == expected
    assert Data("Some data").construct() == "<td>Some data</td>"


# MARK: Row


def test_row_init(
    row: Row,
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> None:
    """Tests the initialization of the Row class."""

    # Test with arguments from fixture
    assert row == row
    assert row.attributes == sample_attributes
    assert row.classes == sample_classes
    assert row.elements == [Data("Test data 1"), Data("Test data 2")]
    assert row.tag == "tr"

    # Test with default arguments
    row = Row()
    assert row == row
    assert row.attributes == Attributes()
    assert row.classes == Classes()
    assert row.elements == Elements()
    assert row.tag == "tr"


def test_row_add(row: Row) -> None:
    """Tests the add method of the Row class."""
    new_data = Data("Test data 3")
    row.add(new_data)
    expected = [
        Data("Test data 1"),
        Data("Test data 2"),
        Data("Test data 3"),
    ]
    assert row.elements == expected
    assert row.elements.elements == expected


def test_row_set(row: Row) -> None:
    """Tests the set method of the Row class."""
    new_data = [Data("Test data 3"), Data("Test data 4")]
    row.set(*new_data)
    assert row.elements == new_data
    assert row.elements.elements == new_data


def test_row_insert(row: Row) -> None:
    """Tests the insert method of the Row class."""
    row.insert(1, Data("Test data 3"))
    expected = [
        Data("Test data 1"),
        Data("Test data 3"),
        Data("Test data 2"),
    ]
    assert row.elements == expected
    assert row.elements.elements == expected
    assert len(row.elements) == len(expected)


def test_row_update(row: Row) -> None:
    """Tests the update method of the Row class."""
    row.update(0, Data("Test data 3"))
    expected = [Data("Test data 3"), Data("Test data 2")]
    assert row.elements == expected
    assert row.elements.elements == expected


def test_row_remove(row: Row) -> None:
    """Tests the remove method of the Row class."""
    row.remove(1)
    expected = [Data("Test data 1")]
    assert row.elements == expected
    assert row.elements.elements == expected
    assert len(row.elements) == len(expected)


def test_row_pop(row: Row) -> None:
    """Tests the pop method of the Row class."""

    # Pop with an integer argument
    row.pop(1)
    expected = [Data("Test data 1")]
    assert row.elements == expected
    assert row.elements.elements == expected

    # Pop with a non-integer argument
    with pytest.raises(TypeError):
        row.pop("1")

    # Pop with no arguments
    row.pop()
    assert row.elements == []
    assert row.elements.elements == []


def test_row_clear(row: Row) -> None:
    """Tests the clear method of the Row class."""
    row.clear()
    assert row.elements == Elements()
    assert row.elements.elements == []


def test_row_construct(row: Row) -> None:
    """Tests the construct method of the Row class."""
    expected = (
        "<tr id='test' disabled class='class-1 class2'>"
        "<td>Test data 1</td>"
        "<td>Test data 2</td>"
        "</tr>"
    )
    assert row.construct() == expected
    assert Row().construct() == "<tr></tr>"


def test_row_iter(row: Row) -> None:
    """Tests the __iter__ method of the Row class."""
    expected = [Data("Test data 1"), Data("Test data 2")]
    assert list(row) == expected
    for actual, expected in zip(row, expected):
        assert actual == expected


# MARK: Header


def test_header_init(
    header: Header,
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> None:
    """Tests the initialization of the Header class."""

    # Test with arguments from fixture
    assert header == header
    assert header.attributes == sample_attributes
    assert header.classes == sample_classes
    assert header.elements == [Data("Test data 1"), Data("Test data 2")]
    assert header.tag == "tr"
    assert all(d.is_header for d in header.elements)

    # Test with default arguments
    header = Header()
    assert header == header
    assert header.attributes == Attributes()
    assert header.classes == Classes()
    assert header.elements == Elements()
    assert header.tag == "tr"
    assert all(d.is_header for d in header.elements)

    # Test with invalid values
    invalid_values = [
        (1, "int"),
        (2.5, "float"),
        ("Test", "str"),
        (True, "bool"),
        (None, "None"),
    ]
    for invalid_value, invalid_type in invalid_values:
        message = f"Expected Data object, got {invalid_type}"
        with pytest.raises(TypeError, match=message):
            Header([Data("Test data"), invalid_value])


def test_header_add(header: Header) -> None:
    """Tests the add method of the Header class."""
    new_data = Data("Test data 3")
    header.add(new_data)
    expected = [
        Data("Test data 1"),
        Data("Test data 2"),
        Data("Test data 3"),
    ]
    assert header.elements == expected
    assert header.elements.elements == expected
    assert all(d.is_header for d in header.elements)


def test_header_set(header: Header) -> None:
    """Tests the set method of the Header class."""
    new_data = [Data("Test data 3"), Data("Test data 4")]
    header.set(*new_data)
    assert header.elements == new_data
    assert header.elements.elements == new_data
    assert all(d.is_header for d in header.elements)


def test_header_insert(header: Header) -> None:
    """Tests the insert method of the Header class."""
    header.insert(1, Data("Test data 3"))
    expected = [
        Data("Test data 1"),
        Data("Test data 3"),
        Data("Test data 2"),
    ]
    assert header.elements == expected
    assert header.elements.elements == expected
    assert len(header.elements) == len(expected)
    assert all(d.is_header for d in header.elements)


def test_header_update(header: Header) -> None:
    """Tests the update method of the Header class."""
    header.update(0, Data("Test data 3"))
    expected = [Data("Test data 3"), Data("Test data 2")]
    assert header.elements == expected
    assert header.elements.elements == expected
    assert all(d.is_header for d in header.elements)


def test_header_construct(header: Header) -> None:
    """Tests the construct method of the Header class."""
    expected = (
        "<tr id='test' disabled class='class-1 class2'>"
        "<th>Test data 1</th>"
        "<th>Test data 2</th>"
        "</tr>"
    )
    assert header.construct() == expected
    assert Header().construct() == "<tr></tr>"


# MARK: Table


def test_table_init(
    table: Table,
    sample_attributes: Attributes,
    sample_classes: Classes,
) -> None:
    """Tests the initialization of the Table class."""

    # Test with arguments from fixture
    assert table == table
    assert table.attributes == sample_attributes
    assert table.classes == sample_classes
    assert table.rows == [
        Row([Data("Test data 1"), Data("Test data 2")]),
        Row([Data("Test data 3"), Data("Test data 4")]),
    ]
    assert table.header == Header([Data("Column 1"), Data("Column 2")])
    assert table.tag == "table"

    # Test with default arguments
    table = Table()
    assert table == table
    assert table.attributes == Attributes()
    assert table.classes == Classes()
    assert table.rows == []
    assert table.header is None
    assert table.tag == "table"

    # Test with only rows
    expected_rows = [
        Row([Data("Test data 1"), Data("Test data 2")]),
        Row([Data("Test data 3"), Data("Test data 4")]),
    ]
    table = Table(rows=expected_rows)
    assert table == table
    assert table.attributes == Attributes()
    assert table.classes == Classes()
    assert table.rows == expected_rows
    assert table.header is None
    assert table.tag == "table"

    # Test with only header
    expected_header = Header([Data("Column 1"), Data("Column 2")])
    table = Table(header=expected_header)
    assert table == table
    assert table.attributes == Attributes()
    assert table.classes == Classes()
    assert table.rows == []
    assert table.header == expected_header
    assert table.tag == "table"


def test_table_header_exists(table: Table) -> None:
    """Tests the _header_exists method of the Table class."""
    assert table._header_exists() is True
    table = Table()
    assert table._header_exists() is False


def test_table_header(table: Table) -> None:
    """Tests the header property of the Table class."""

    # Test the getter
    assert table.header == Header([Data("Column 1"), Data("Column 2")])
    assert all(d.is_header for d in table.header)

    # Test the setter
    expected_header = Header([Data("Column 3"), Data("Column 4")])
    table.header = expected_header
    assert table.header == expected_header
    assert all(d.is_header for d in table.header)

    # Test the setter with invalid type
    message = "Expected Header object, got int"
    with pytest.raises(TypeError, match=message):
        table.header = 1

    # Test the setter with no existing header
    table = Table()
    assert table.header is None
    table.header = expected_header
    assert table.header == expected_header
    assert all(d.is_header for d in table.header)


def test_table_rows(table: Table) -> None:
    """Tests the rows property of the Table class."""

    # Test the getter
    assert table.rows == [
        Row([Data("Test data 1"), Data("Test data 2")]),
        Row([Data("Test data 3"), Data("Test data 4")]),
    ]
    assert all(not r.is_header for row in table.rows for r in row)

    # Test the setter
    expected_rows = [
        Row([Data("Test data 5"), Data("Test data 6")]),
        Row([Data("Test data 7"), Data("Test data 8")]),
    ]
    table.rows = expected_rows
    assert table.rows == expected_rows
    assert all(not r.is_header for row in table.rows for r in row)

    # Test the setter with invalid type
    message = "Expected Row object, got int"
    with pytest.raises(TypeError, match=message):
        table.rows = [Row([Data("Test data 9")]), 10]


def test_table_set_header(table: Table) -> None:
    """Tests the set_header method of the Table class."""
    expected_header = Header([Data("Column 3"), Data("Column 4")])
    table.set_header(expected_header)
    assert table.header == expected_header
    assert all(d.is_header for d in table.header)

    # Test with invalid type
    message = "Expected Header object, got dict"
    with pytest.raises(TypeError, match=message):
        table.set_header(dict())

    # Test with no existing header
    table = Table()
    assert table.header is None
    table.set_header(expected_header)
    assert table.header == expected_header
    assert all(d.is_header for d in table.header)


def test_table_clear_header(table: Table) -> None:
    """Tests the clear_header method of the Table class."""
    assert table.header is not None
    table.clear_header()
    assert table.header is None


def test_table_add_rows(table: Table) -> None:
    """Tests the add_rows method of the Table class."""
    new_rows = [
        Row([Data("Test data 5"), Data("Test data 6")]),
        Row([Data("Test data 7"), Data("Test data 8")]),
    ]
    table.add_rows(*new_rows)
    expected_rows = [
        Row([Data("Test data 1"), Data("Test data 2")]),
        Row([Data("Test data 3"), Data("Test data 4")]),
        *new_rows,
    ]
    assert table.rows == expected_rows
    assert all(not r.is_header for row in table.rows for r in row)

    # Test with invalid type
    message = "Expected Row object, got tuple"
    with pytest.raises(TypeError, match=message):
        table.add_rows(tuple(), dict())


def test_table_set_rows(table: Table) -> None:
    """Tests the set_rows method of the Table class."""

    # Test with an existing header
    new_rows = [
        Row([Data("Test data 5"), Data("Test data 6")]),
        Row([Data("Test data 7"), Data("Test data 8")]),
    ]
    table.set_rows(*new_rows)
    assert table.header is not None
    assert table.rows == new_rows
    assert all(not r.is_header for row in table.rows for r in row)

    # Test with invalid type
    message = "Expected Row object, got set"
    with pytest.raises(TypeError, match=message):
        table.set_rows(set(), None)

    # Test with no existing header
    table = Table()
    table.set_rows(*new_rows)
    assert table.header is None
    assert table.rows == new_rows
    assert all(not r.is_header for row in table.rows for r in row)


def test_table_clear_rows(table: Table) -> None:
    """Tests the clear_rows method of the Table class."""
    assert table.rows == [
        Row([Data("Test data 1"), Data("Test data 2")]),
        Row([Data("Test data 3"), Data("Test data 4")]),
    ]
    table.clear_rows()
    assert table.rows == []
    assert table.header is not None


def test_table_clear(table: Table) -> None:
    """Tests the clear method of the Table class."""
    assert table.rows != []
    assert table.header is not None
    table.clear()
    assert table.rows == []
    assert table.header is None
    # Clear again to verify there are no raised errors
    table.clear()
    assert table.rows == []
    assert table.header is None


def test_table_construct(table: Table) -> None:
    """Tests the construct method of the Table class."""
    expected = (
        "<table id='test' disabled class='class-1 class2'>"
        "<tr>"
        "<th>Column 1</th>"
        "<th>Column 2</th>"
        "</tr>"
        "<tr>"
        "<td>Test data 1</td>"
        "<td>Test data 2</td>"
        "</tr>"
        "<tr>"
        "<td>Test data 3</td>"
        "<td>Test data 4</td>"
        "</tr>"
        "</table>"
    )
    assert table.construct() == expected
    assert Table().construct() == "<table></table>"


def test_table_raise_if_incorrect_type(table: Table) -> None:
    """Tests the _raise_if_incorrect_type method of the Table class."""

    # Test with correct type
    table._raise_if_incorrect_type(1, expected_type=int)

    # Test with incorrect type
    message = "Expected int object, got str"
    with pytest.raises(TypeError, match=message):
        table._raise_if_incorrect_type("Test", expected_type=int)


def test_table_from_df(sample_df: pd.DataFrame) -> None:
    """Tests the from_df method of the Table class."""

    # Test default arguments
    table = Table.from_df(sample_df)
    expected_attributes = Attributes()
    expected_rows = [
        Row(
            [
                Data(1, classes=Classes("A")),
                Data(4, classes=Classes("B")),
                Data(7, classes=Classes("C")),
            ],
            classes=Classes("odd"),
        ),
        Row(
            [
                Data(2, classes=Classes("A")),
                Data(5, classes=Classes("B")),
                Data(8, classes=Classes("C")),
            ],
            classes=Classes("even"),
        ),
        Row(
            [
                Data(3, classes=Classes("A")),
                Data(6, classes=Classes("B")),
                Data(9, classes=Classes("C")),
            ],
            classes=Classes("odd"),
        ),
    ]
    expected_header = Header([Data("A"), Data("B"), Data("C")])
    assert table.rows == expected_rows
    assert table.header == expected_header
    assert table.attributes == expected_attributes

    # Test with table classes
    expected_attributes = Attributes({"class": "test"})
    table = Table.from_df(sample_df, table_classes=Classes("test"))
    expected_rows = [
        Row(
            [
                Data(1, classes=Classes("A")),
                Data(4, classes=Classes("B")),
                Data(7, classes=Classes("C")),
            ],
            classes=Classes("odd"),
        ),
        Row(
            [
                Data(2, classes=Classes("A")),
                Data(5, classes=Classes("B")),
                Data(8, classes=Classes("C")),
            ],
            classes=Classes("even"),
        ),
        Row(
            [
                Data(3, classes=Classes("A")),
                Data(6, classes=Classes("B")),
                Data(9, classes=Classes("C")),
            ],
            classes=Classes("odd"),
        ),
    ]
    assert table.rows == expected_rows
    assert table.header == expected_header
    assert table.attributes == expected_attributes

    # Test with header classes
    table = Table.from_df(sample_df, header_classes=Classes("test"))
    expected_attributes = Attributes()
    expected_header = Header(
        [Data("A"), Data("B"), Data("C")],
        classes=Classes("test"),
    )
    assert table.rows == expected_rows
    assert table.header == expected_header
    assert table.attributes == expected_attributes

    # Test with body classes
    table = Table.from_df(sample_df, body_classes=Classes("test"))
    expected_rows = [
        Row(
            [
                Data(1, classes=Classes("A")),
                Data(4, classes=Classes("B")),
                Data(7, classes=Classes("C")),
            ],
            classes=Classes("test", "odd"),
        ),
        Row(
            [
                Data(2, classes=Classes("A")),
                Data(5, classes=Classes("B")),
                Data(8, classes=Classes("C")),
            ],
            classes=Classes("test", "even"),
        ),
        Row(
            [
                Data(3, classes=Classes("A")),
                Data(6, classes=Classes("B")),
                Data(9, classes=Classes("C")),
            ],
            classes=Classes("test", "odd"),
        ),
    ]
    expected_header = Header([Data("A"), Data("B"), Data("C")])
    assert table.rows == expected_rows
    assert table.header == expected_header
    assert table.attributes == expected_attributes

    # Test without alternating rows
    table = Table.from_df(sample_df, alternating_rows=False)
    expected_rows = [
        Row(
            [
                Data(1, classes=Classes("A")),
                Data(4, classes=Classes("B")),
                Data(7, classes=Classes("C")),
            ],
        ),
        Row(
            [
                Data(2, classes=Classes("A")),
                Data(5, classes=Classes("B")),
                Data(8, classes=Classes("C")),
            ],
        ),
        Row(
            [
                Data(3, classes=Classes("A")),
                Data(6, classes=Classes("B")),
                Data(9, classes=Classes("C")),
            ],
        ),
    ]
    assert table.rows == expected_rows
    assert table.header == expected_header
    assert table.attributes == expected_attributes

    # Test without columns as classes
    table = Table.from_df(sample_df, columns_as_classes=False)
    expected_rows = [
        Row([Data(1), Data(4), Data(7)], classes=Classes("odd")),
        Row([Data(2), Data(5), Data(8)], classes=Classes("even")),
        Row([Data(3), Data(6), Data(9)], classes=Classes("odd")),
    ]
    assert table.rows == expected_rows
    assert table.header == expected_header
    assert table.attributes == expected_attributes

    # Test with attributes
    expected_attributes = Attributes({"id": "test"})
    table = Table.from_df(sample_df, attributes=expected_attributes)
    expected_rows = [
        Row(
            [
                Data(1, classes=Classes("A")),
                Data(4, classes=Classes("B")),
                Data(7, classes=Classes("C")),
            ],
            classes=Classes("odd"),
        ),
        Row(
            [
                Data(2, classes=Classes("A")),
                Data(5, classes=Classes("B")),
                Data(8, classes=Classes("C")),
            ],
            classes=Classes("even"),
        ),
        Row(
            [
                Data(3, classes=Classes("A")),
                Data(6, classes=Classes("B")),
                Data(9, classes=Classes("C")),
            ],
            classes=Classes("odd"),
        ),
    ]
    assert table.rows == expected_rows
    assert table.header == expected_header
    assert table.attributes == expected_attributes
