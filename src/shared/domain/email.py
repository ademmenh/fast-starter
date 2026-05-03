from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    Shared value object for e-mail addresses.
    Normalises to lowercase, trims whitespace, validates format.
    """

    value: str

    @classmethod
    def create(cls, raw: str) -> Email:
        normalized = raw.strip().lower()
        pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        if not re.match(pattern, normalized):
            raise ValueError(f"Invalid email format: {raw!r}")
        return cls(value=normalized)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"Email({self.value!r})"
