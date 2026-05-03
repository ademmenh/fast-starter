from dataclasses import dataclass


@dataclass(frozen=True)
class Password:
    value: str

    @classmethod
    def create(cls, raw: str) -> "Password":
        if len(raw) < 6:
            raise ValueError("Password must be at least 6 characters")
        return cls(value=raw)
