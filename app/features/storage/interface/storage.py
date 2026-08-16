from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class Storage(ABC):

    @abstractmethod
    async def save(self, file: AsyncIterator[bytes], *, key: str) -> None:
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        ...

    @abstractmethod
    async def exist(self, key: str) -> bool:
        ...

    @abstractmethod
    async def read(self, *, key: str) -> AsyncIterator[bytes]:
        ...
