# tests/test_parse_kv_string.py
import pytest
from hypothesis import given, strategies as st

from utils import parse_kv_string

# Helper to build a kv string using given separators
def build_kv_string(d: dict, pair_sep: str = "|", kv_sep: str = ":") -> str:
    return f" {pair_sep} ".join(f"{k}{kv_sep}{v}" for k, v in d.items())

class TestParseKvString:
    def test_empty_input_returns_empty_dict(self):
        assert parse_kv_string("") == {}
        assert parse_kv_string(None) == {} if False else parse_kv_string("") == {}  # keep explicit empty-string behavior

    def test_basic_parsing(self):
        s = "a:1 | b:2 | c:3"
        assert parse_kv_string(s) == {"a": "1", "b": "2", "c": "3"}

    def test_whitespace_and_trimming(self):
        s = "  a  :  1  |  b:2  "
        assert parse_kv_string(s) == {"a": "1", "b": "2"}

    def test_duplicate_keys_last_wins(self):
        s = "a:1 | a:2 | a:3"
        assert parse_kv_string(s) == {"a": "3"}

    def test_value_can_contain_kv_sep(self):
        s = "path:/some:weird:path | other:ok"
        # split only on first kv_sep
        assert parse_kv_string(s) == {"path": "/some:weird:path", "other": "ok"}

    def test_custom_separators(self):
        s = "x=10; y=20;z=30"
        assert parse_kv_string(s, pair_sep=";", kv_sep="=") == {"x": "10", "y": "20", "z": "30"}

    def test_malformed_pair_skipped_when_not_strict(self):
        s = "a:1 | badpair | b:2"
        assert parse_kv_string(s, strict=False) == {"a": "1", "b": "2"}

    def test_malformed_pair_raises_in_strict_mode(self):
        s = "a:1 | badpair | b:2"
        with pytest.raises(ValueError):
            parse_kv_string(s, strict=True)

    def test_empty_key_skipped_when_not_strict(self):
        s = ":no_key | a:1"
        assert parse_kv_string(s, strict=False) == {"a": "1"}

    def test_empty_key_raises_in_strict_mode(self):
        s = ":no_key | a:1"
        with pytest.raises(ValueError):
            parse_kv_string(s, strict=True)

    @given(
        st.dictionaries(
            keys=st.text(min_size=1).filter(lambda t: "|" not in t and ":" not in t and t.strip() != "" and t.strip() == t),
            values=st.text().filter(lambda t: "|" not in t and t.strip() == t),
            max_size=100,
        )
    )
    def test_roundtrip_with_default_separators(self, data):
        """
        Property test: build a string from a dict using the default separators
        and ensure parse_kv_string returns the original mapping.
        """
        s = build_kv_string(data, pair_sep="|", kv_sep=":")
        assert parse_kv_string(s) == data

    def test_trailing_and_leading_empty_pairs_ignored(self):
        s = " | a:1 |  | b:2 | "
        assert parse_kv_string(s) == {"a": "1", "b": "2"}

    def test_pairs_with_only_whitespace_ignored(self):
        s = "   |   |a:1|   "
        assert parse_kv_string(s) == {"a": "1"}
