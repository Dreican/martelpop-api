from typing import Annotated

from fastapi import Depends

from app.core.services.slug_service import SlugService


def get_slug_service() -> SlugService:
    return SlugService()


SlugServiceDep = Annotated[
    SlugService,
    Depends(get_slug_service),
]
