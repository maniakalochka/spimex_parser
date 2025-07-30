from abc import ABC, abstractmethod
from typing import Any


class BasePageParser(ABC):
    BASE_URL: str

    @abstractmethod
    async def parse(self, raw_input: Any) -> list[dict]:
        raise NotImplementedError("Subclasses must implement this method")

class BaseExcelParser(ABC):

    @abstractmethod
    def parse(self, raw_input: bytes) -> list[dict]:
        raise NotImplementedError("Subclasses must implement this method")
