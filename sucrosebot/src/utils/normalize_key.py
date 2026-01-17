import re

def normalize_key(value: str) -> str:
    """
    Normalize user input so it maps to a single canonical key.
    """
    if not value:
        return ""

    # Remove surrounding quotes
    value = value.strip().strip('"').strip("'")

    # Lowercase
    value = value.lower()

    # Replace multiple spaces with one
    value = re.sub(r"\s+", " ", value)

    # Remove non-alphanumeric (keep spaces)
    value = re.sub(r"[^a-z0-9 ]", "", value)

    return value.strip()
