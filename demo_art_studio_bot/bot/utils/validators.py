import re


PHONE_PATTERN = re.compile(r"^[+\d][\d\s\-()]{6,}$")


def is_valid_contact(value: str) -> bool:
    value = value.strip()
    if value.startswith("@") and len(value) > 1:
        return True
    return bool(PHONE_PATTERN.match(value))
