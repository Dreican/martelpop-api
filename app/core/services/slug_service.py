from collections.abc import Callable, Awaitable

from slugify import slugify


class SlugService:

    @staticmethod
    def _create(*parts: str) -> str:
        return slugify("-".join(parts))

    async def create_unique(self, *parts: str, slug_exists: Callable[[str], Awaitable[bool]]) -> str:
        base = SlugService._create(*parts)
        slug = base
        counter = 2

        while await slug_exists(slug):
            slug = f"{base}-{counter}"
            counter += 1

        return slug
