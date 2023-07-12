from abc import ABC, abstractmethod
from typing import Any

class IAbstractAgent:

    @abstractmethod
    def __call__(self, query: str, *args: Any, **kwds: Any) -> Any:
        pass