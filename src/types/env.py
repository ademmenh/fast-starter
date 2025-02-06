from enum import Enum

class enEnv (str, Enum):
    prod = "prod"
    dev = "dev"
    test = "test"

    def __str__ (self):
        return self.value
