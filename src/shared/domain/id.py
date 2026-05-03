from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Id:
    """
    Domain value object for entity identifiers.
    Wraps a UUID string and guarantees format validity.
    """

    value: str

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"Id({self.value!r})"

    @classmethod
    def from_str(cls, value: str) -> Id:
        """Parse an existing UUID string into an Id."""
        return cls(value=value)
