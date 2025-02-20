"""
Contains code for all table-related HTML elements.
"""

from __future__ import annotations

from typing import Any, Self

from ..core import HTMLBuilder
from ..utilities import requires_modules

# Import optional dependencies
try:
    import numpy as np
except ImportError:
    pass

try:
    import pandas as pd
except ImportError:
    pass


class Data(HTMLBuilder):
    """Constructs an HTML table data."""

    def __init__(
        self,
        data: list[Any],
        classes: str | list[str] | None = None,
        is_header: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initializes the Data object."""

        # Initialize the builder
        super().__init__(classes=classes, **kwargs)
        self.tag = "td" if not is_header else "th"

        # Store instance variables
        self._is_header = is_header

        # Set the data
        self.set_data(data)

    def set_data(self, data: Any) -> None:
        """Sets the data."""
        self.clear_elements()
        self.add_element(data)

    def construct(self) -> str:
        """Generates HTML from the stored elements."""

        # Open the tag
        html = f"<{self.tag}{self.attributes_to_string()}>"

        # Add the data
        for element in self.elements:
            html += f"{element}"

        # Close the tag and return the HTML
        html += f"</{self.tag}>"
        return html


class Row(HTMLBuilder):
    """Constructs an HTML table row."""

    def __init__(
        self,
        data: Any | list[Any],
        classes: str | list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initializes the Row object."""

        # Initialize the builder
        super().__init__(classes=classes, **kwargs)
        self.tag = "tr"

        # Set the data
        self.set_data(data)

    def add_data(self, data: Any) -> None:
        """Adds data."""
        self.add_element(data)

    def set_data(self, data: Any | list[Any]) -> None:
        """Sets the data."""
        self.clear_elements()
        if isinstance(data, list):
            self.add_elements(data)
        else:
            self.add_element(data)

    def construct(self) -> str:
        """Generates HTML from the stored elements."""

        # Open the tag
        html = f"<{self.tag}{self.attributes_to_string()}>"

        # Add the data
        for element in self.elements:
            if isinstance(element, Data):
                html += f"{element}"
            else:
                html += f"<td>{element}</td>"

        # Close the tag and return the HTML
        html += f"</{self.tag}>"
        return html


class Header(Row):
    """Constructs an HTML table header row.

    Simple wrapper around the Row class.
    """

    def __init__(
        self,
        data: list[Any],  # TODO: Implement span?
        classes: str | list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initializes the Header object."""

        # Initialize the builder
        super().__init__(data, classes=classes, **kwargs)

    def construct(self) -> str:
        """Generates HTML from the stored elements."""

        # Open the tag
        html = f"<{self.tag}{self.attributes_to_string()}>"

        # Add the data
        for element in self.elements:
            if isinstance(element, Data):
                html += f"{element}"
            else:
                html += f"<th>{element}</th>"

        # Close the tag and return the HTML
        html += f"</{self.tag}>"
        return html


class Table(HTMLBuilder):
    """Constructs an HTML table."""

    def __init__(
        self,
        data: list[Row] | list[list[Any]],
        header: Header | Row | None = None,
        classes: str | list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initializes the Table object."""

        # Initialize the builder
        super().__init__(classes=classes, **kwargs)
        self.tag = "table"

        # Add header and data
        self.add_data(data)
        self.add_header(header)

    def _header_exists(self) -> bool:
        """Determines whether or not a header exists in the stored data."""
        return self.elements and isinstance(self.elements[0], Header)

    @property
    def header(self) -> Header | Row | None:
        """Gets the header if one exists."""
        return self.elements[0] if self._header_exists() else None

    @header.setter
    def header(self, value: Header | Row | None) -> None:
        """Sets the header row."""
        self.update_header(value)

    def add_header(self, header: Header | Row | None) -> None:
        """Adds a header to the table."""
        if not header:
            return
        elif not self._header_exists():
            self.insert_element(0, header)
        else:
            self.update_header(header)

    def remove_header(self) -> Header | Row | None:
        """Removes the header row and returns it if one existed."""
        if self._header_exists():
            return self.remove_element(0)

    def update_header(self, header: Header | Row | None) -> None:
        """Updates the header of the table."""
        if self._header_exists():
            self.update_element(0, header)
        else:
            self.insert_element(0, header)

    def add_data(self, data: list[Row] | list[list[Any]]) -> None:
        """Adds data."""
        for item in data:
            # TODO: Account for Header?
            # Convert to a row object if necessary
            if not isinstance(item, Row):
                item = Row(item)
            self.add_element(item)

    def set_data(self, data: list[Any]) -> None:
        """Sets the data."""
        self.clear_data()
        self.add_data(data)

    def clear_data(self) -> None:
        """Clears the data."""
        if header := self.remove_header():
            self.clear_elements()
            self.add_header(header)
        else:
            self.clear_elements()

    def clear(self) -> None:
        """Clears both the header and the data."""
        self.remove_header()
        self.clear_data()

    def construct(self) -> str:
        """Generates HTML from the stored elements."""

        # Open the tag
        html = f"<{self.tag}{self.attributes_to_string()}>"

        # Add the data
        for element in self.elements:
            html += f"{element}"

        # Close the tag and return the HTML
        html += f"</{self.tag}>"
        return html

    @classmethod
    @requires_modules("pandas", "numpy")
    def from_df(
        cls,
        df: pd.DataFrame,
        table_classes: str | list[str] | None = None,
        header_classes: str | list[str] | None = None,
        body_classes: str | list[str] | None = None,
        alternating_rows: bool = True,
        columns_as_classes: bool = True,
        **kwargs: Any,
    ) -> Self:
        """Creates an HTMLTable object from a pandas dataframe.

        Setting alternating_rows to True will add alternating classes to each
        row (excluding the header) for styling purposes. Even-numbered rows
        will have the class 'even' added and odd-numbered rows will have the
        class 'odd' added.
        """

        # Reset the index for the dataframe
        if alternating_rows:
            df.index = np.arange(1, len(df) + 1)

        # Create the body
        body = []
        for r, row in df.iterrows():
            data = []
            for i, item in enumerate(row):
                data_classes = []
                if columns_as_classes:
                    data_classes.append(row.index[i])  # TODO: Sanitize name
                data.append(Data(item, classes=data_classes))
            html_row = Row(data, classes=body_classes)
            if alternating_rows:
                html_row.add_class("odd" if r % 2 != 0 else "even")
            body.append(html_row)

        # Create the header
        header = Header(df.columns.to_list(), classes=header_classes)

        # Create an instance with the results and return
        return cls(body, header, classes=table_classes, **kwargs)
