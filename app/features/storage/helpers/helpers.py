from urllib.parse import quote
from uuid import UUID

from unicodedata import normalize

from app.core.config.configuration import get_config

config = get_config()
FILE_URL_PREFIX = f"{config.app.api_prefix}/files"


def content_disposition_filename(filename: str) -> str:
    filename = normalize("NFC", filename)

    fallback = (
        normalize("NFKD", filename)
        .encode("ascii", "ignore")
        .decode("ascii")
        .replace("\\", "_")
        .replace('"', "_")
        .replace("\r", "_")
        .replace("\n", "_")
    )

    encoded = quote(
        filename,
        safe="!#$&+-.^_`|~",
    )

    return f'attachment; filename="{fallback}"; filename*=UTF-8''{encoded}'


def public_file_url(file_id: UUID | None) -> str | None:
    if file_id is None:
        return None

    return f"{FILE_URL_PREFIX}/{file_id}"