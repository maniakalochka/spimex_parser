from abc import ABC, abstractmethod
from typing import Any


class BaseParser(ABC):
    BASE_URL: str

    @abstractmethod
    def parse(self, raw_input: Any) -> list[dict]:
        raise NotImplementedError("Subclasses must implement this method")
