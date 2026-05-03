from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Phone:
    """
    Shared value object for phone numbers.
    Accepts an optional leading '+', followed by digits, spaces, hyphens,
    and parentheses.  Strips surrounding whitespace; stores as-is otherwise.
    Minimum 7, maximum 20 characters (after stripping).
    """

    value: str

    @classmethod
    def create(cls, raw: str) -> Phone:
        normalized = raw.strip()
        pattern = r"^\+?[\d\s\-\(\)]{7,20}$"
        if not re.match(pattern, normalized):
            raise ValueError(f"Invalid phone number format: {raw!r}")
        return cls(value=normalized)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Phone):
            return NotImplemented
        return self.value == other.value
