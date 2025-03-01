"""
Contains types for the package.
"""

from typing import Any, TypeAlias

from .attributes import Attributes, Classes, Elements

# MARK: Classes

ClassesType: TypeAlias = Classes | str

# MARK: Attributes

AttributeValue: TypeAlias = str | bool | None
AttributeMap: TypeAlias = dict[str, AttributeValue]
AttributesType: TypeAlias = Attributes | AttributeMap

# MARK: Elements

Element: TypeAlias = Any
ElementsType: TypeAlias = Elements | list[Element]
