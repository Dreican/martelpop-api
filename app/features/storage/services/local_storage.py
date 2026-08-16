import asyncio
from collections.abc import AsyncIterator
from pathlib import Path

from app.features.storage.interface.storage import Storage


class LocalStorage(Storage):

    def __init__(self, base_path: Path, *, chunk_size: int = 1024 * 1024) -> None:
        self._base_path = base_path
        self._chunk_size = chunk_size
        self._base_path.mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, key: str) -> Path:
        path = (self._base_path / key).resolve()

        if not path.is_relative_to(self._base_path.resolve()):
            raise ValueError(f"Path {path} is not within {self._base_path}")

        return path

    async def save(self, file: AsyncIterator[bytes], *, key: str) -> None:
        path = self._resolve_path(key)

        path.parent.mkdir(parents=True, exist_ok=True)

        temporary_path = path.with_name(
            f".{path.name}.tmp"
        )
        try:
            with temporary_path.open("wb") as destination:
                async for chunk in file:
                    await asyncio.to_thread(
                        destination.write,
                        chunk
                    )

            await asyncio.to_thread(
                temporary_path.replace,
                path
            )

        except Exception:
            await asyncio.to_thread(
                temporary_path.unlink,
                missing_ok=True
            )
            raise

    async def delete(self, key: str) -> None:
        path = self._resolve_path(key)
        await asyncio.to_thread(
            path.unlink,
            missing_ok=True
        )

    async def exist(self, key: str) -> bool:
        path = self._resolve_path(key)
        return await asyncio.to_thread(
            path.is_file
        )

    async def read(self, *, key: str) -> AsyncIterator[bytes]:
        path = self._resolve_path(key)

        with path.open("rb") as source:
            while True:
                chunk = await asyncio.to_thread(
                    source.read,
                    self._chunk_size,
                )

                if not chunk:
                    break

                yield chunk