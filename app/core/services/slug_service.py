from collections.abc import Callable, Awaitable

from slugify import slugify


class SlugService:
    @staticmethod
    def create(*parts: str) -> str:
        return slugify("-".join(parts))

    @staticmethod
    async def create_unique(*parts: str, exists: Callable[[str], Awaitable[bool]]) -> str:
        base = SlugService.create(*parts)
        slug = base
        counter = 2

        while await exists(slug):
            slug = f"{base}-{counter}"
            counter += 1

        return slug
