"""
Contains tests for the utilities.optional module.
"""

from unittest.mock import patch

import pytest

from balisage.utilities.optional import module_exists, requires_modules


def test_module_exists() -> None:
    """Tests the module_exists function."""

    # Test with built-in modules
    assert module_exists("sys") is True
    assert module_exists("os") is True

    # Test with non-existent modules
    assert module_exists("does_not_exist") is False

    # Test with a third-party module
    try:
        import pandas  # noqa: F401

        pandas_installed = True
    except ImportError:
        pandas_installed = False
    assert module_exists("pandas") is (True if pandas_installed else False)

    # Simulate an Import or ModuleNotFound error
    with patch("importlib.import_module", side_effect=ImportError):
        assert module_exists("balisage") is False
    with patch("importlib.import_module", side_effect=ModuleNotFoundError):
        assert module_exists("balisage") is False


def test_requires_modules() -> None:
    """Tests the requires_modules decorator."""

    # Verify normal execution when all modules are present
    @requires_modules("sys", "os")
    def test_function() -> str:
        return "Success"

    assert test_function() == "Success"

    # Verify error when some modules are missing
    with patch("balisage.utilities.optional.module_exists") as mock:
        mock.side_effect = lambda module: module != "does_not_exist"

        @requires_modules("sys", "does_not_exist")
        def test_function() -> str:
            return "Success"

        for error in [ImportError, ModuleNotFoundError]:
            with pytest.raises(error):
                test_function()

    # Verify error when all modules are missing
    with patch("balisage.utilities.optional.module_exists", return_value=False):

        @requires_modules("does_not_exist_1", "does_not_exist_2")
        def test_function() -> str:
            return "Success"

        for error in [ImportError, ModuleNotFoundError]:
            with pytest.raises(error):
                test_function()
