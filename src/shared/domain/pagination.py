from dataclasses import dataclass


@dataclass
class PaginationParams:
    page: int = 1
    limit: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit
