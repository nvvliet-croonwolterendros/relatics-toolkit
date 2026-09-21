import pytest
import pandas as pd

from relatics_toolkit.utils.utils import normalize_value

@pytest.mark.parametrize("val", [None, float("nan"), pd.NaT, pd.NA])
def test_na_like_inputs_return_empty_string(val):
    assert normalize_value(val) == None


@pytest.mark.parametrize("val", ["", "!!!", "   ", "🎉"])
def test_values_that_normalize_to_nothing_return_empty_string(val):
        with pytest.raises(RuntimeError, match="got normalized to empty string"):
            normalize_value(val)

@pytest.mark.parametrize(
    ("val", "expected"),
    [
        ("Hello World", "hello_world"),
        ("Route 66", "route_66"),
        ("a-b-c", "a_b_c"),
        ("foo(bar)", "foo_bar"),
        ("  hello   world  ", "hello_world"),
    ],
)
def test_general_normalization(val, expected):
    assert normalize_value(val) == expected


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        ("Tom & Jerry", "tom_and_jerry"),
        ("AT&T", "at_and_t"),
        ("a+b", "a_plus_b"),
        ("x=y", "x_is_y"),
        ("korting 50% ", "korting_50_percent"),
        ("C#", "c_nr"),
        ("€5", "euro_5"),           # replacement's leading "_" gets stripped
        ("$100", "dollar_100"),
        ("§ 3.1", "paragraph_3_1"),
        ("°C", "degree_c"),
        ("€&$", "euro_and_dollar"),  # adjacent specials don't stack underscores
    ],
)
def test_special_character_replacements(val, expected):
    assert normalize_value(val) == expected

@pytest.mark.parametrize(
    ("val", "expected"),
    [
        ("Café", "cafe"),
        ("naïve", "naive"),
        ("Ångström", "angstrom"),
        ("a🎉b", "ab"),  # emoji is *removed*, not turned into "_"
    ],
)
def test_unicode_handling(val, expected):
    assert normalize_value(val) == expected

@pytest.mark.parametrize(
    ("val", "expected"),
    [
        ("2024", "no_num_2024"),
        ("42 answers", "no_num_42_answers"),
        ("1+1", "no_num_1_plus_1"),
        ("20°C", "no_num_20_degree_c"),
        ("route 66", "route_66"),  # non-leading digit: no prefix
    ],
)
def test_leading_digit_gets_no_num_prefix(val, expected):
    assert normalize_value(val) == expected


def test_default_max_length_is_63():
    result = normalize_value("x" * 100)
    assert result == "x" * 63
    assert len(result) == 63


def test_custom_max_length():
    assert normalize_value("abcdefghij", max_length=5) == "abcde"


def test_no_num_prefix_counts_towards_max_length():
    # "no_num_" is 7 chars, so 63 - 7 = 56 digits survive truncation
    result = normalize_value("9" * 70)
    assert result == "no_num_" + "9" * 56

@pytest.mark.parametrize(
    ("val", "expected"),
    [
        (123, "no_num_123"),
        (12.5, "no_num_12_5"),
        ("7", "no_num_7"),
    ],
)
def test_non_string_input_is_coerced_via_str(val, expected):
    assert normalize_value(val) == expected

def test_real_world_messy_string():
    val = "H&M — Zomercollectie 2024 (50% korting!)"
    assert normalize_value(val) == "h_and_m_zomercollectie_2024_50_percent_korting"

def testnormalize_value_raise_when_empty_string():
    """Raises when val is empty string"""
    val = ""

    with pytest.raises(RuntimeError, match="got normalized to empty string"):
        normalize_value(val)


def testnormalize_value_raise_when_normalized_to_empty():
    """Raises when val is normalized to empty string"""
    val = "!"

    with pytest.raises(RuntimeError, match="got normalized to empty string"):
        normalize_value(val)
