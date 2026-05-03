import uuid
from src.shared.domain.id import Id


class IDGenerator:
    """
    Infrastructure service that generates unique entity identifiers.
    Keeps ID creation out of models so the application layer owns
    the entity's identity from birth.
    """

    def generate(self) -> Id:
        return Id(value=str(uuid.uuid4()))
