import pytest

from relatics_toolkit.utils.utils import normalize_value


def test_normalize_value_raise_when_empty_string():
    """Raises when val is empty string"""
    val = ""

    with pytest.raises(RuntimeError, match="got normalized to empty string"):
        normalize_value(val)


def test_normalize_value_raise_when_normalized_to_empty():
    """Return None when None is passed"""
    val = "!"

    with pytest.raises(RuntimeError, match="got normalized to empty string"):
        normalize_value(val)
