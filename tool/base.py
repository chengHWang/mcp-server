# tool/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, AsyncGenerator

class BaseTool(ABC):
    name: str
    description: str
    parameters: Dict[str, Any]

    @abstractmethod
    async def __call__(self, arguments: Dict[str, Any], session_id: str = None) -> AsyncGenerator[Dict, None]:
        raise NotImplementedError