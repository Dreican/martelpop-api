from collections.abc import Callable, Awaitable

from slugify import slugify


class SlugService:

    def create(*parts: str) -> str:
        return slugify("-".join(parts))

    async def create_unique(*parts: str, slug_exists: Callable[[str], Awaitable[bool]]) -> str:
        base = SlugService.create(*parts)
        slug = base
        counter = 2

        while await slug_exists(slug):
            slug = f"{base}-{counter}"
            counter += 1

        return slug
