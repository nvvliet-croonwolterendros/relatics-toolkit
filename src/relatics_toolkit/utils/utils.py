import re
import unicodedata

import pandas as pd


def normalize_value(val: str | None, max_length: int = 63) -> str | None:
    """
    Normalize text for use as SQL table and column names.
    """
    original_val = val

    if pd.isna(val) or val is None:
        return None

    val = str(val)

    # Replace special characters
    val = val.replace("&", "_en_").replace("€", "_euro_").replace("+", "_plus_")

    # Unicode -> ASCII
    val = unicodedata.normalize("NFKD", val)
    val = val.encode("ascii", "ignore").decode("ascii")

    # Lowercase
    val = val.lower()

    # Replace invalid characters
    val = re.sub(r"[^a-z0-9_]", "_", val)

    # Collapse underscores
    val = re.sub(r"_+", "_", val)

    # Strip leading/trailing underscores
    val = val.strip("_")

    if not val:
        raise RuntimeError(f"{original_val} got normalized to empty string")

    # Prevent leading digit
    if val[0].isdigit():
        val = f"no_num_{val}"

    # Trim to PostgreSQL identifier length
    return val[:max_length]
