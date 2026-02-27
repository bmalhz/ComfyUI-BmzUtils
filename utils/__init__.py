"""Utils module."""
from typing import Dict


def parse_kv_string(s: str, pair_sep: str = "|", kv_sep: str = ":", strict: bool = False) -> Dict[str, str]:
    """
    Parse a string of key:value pairs separated by pair_sep into a dict.

    Args:
        s: input string, e.g. "a:1 | b:2 | c:3"
        pair_sep: separator between pairs (default '|')
        kv_sep: separator between key and value (default ':')
        strict: if True, raise ValueError on malformed pairs; if False, skip them

    Returns:
        dict mapping keys (str) to values (str)
    """
    if not s:
        return {}

    result = {}
    for raw_pair in s.split(pair_sep):
        pair = raw_pair.strip()
        if not pair:
            continue
        if kv_sep not in pair:
            if strict:
                raise ValueError(f"Malformed pair (missing '{kv_sep}'): {pair!r}")
            else:
                continue
        key, value = pair.split(kv_sep, 1)
        key = key.strip()
        value = value.strip()
        if key == "":
            if strict:
                raise ValueError(f"Empty key in pair: {pair!r}")
            else:
                continue
        result[key] = value
    return result
