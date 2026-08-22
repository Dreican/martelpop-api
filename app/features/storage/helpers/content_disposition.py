from urllib.parse import quote

from unicodedata import normalize


def content_disposition_attachment(filename: str) -> str:
    return f'attachment; {_content_disposition(filename)}'


def content_disposition_inline(filename: str) -> str:
    return f'inline; {_content_disposition(filename)}'


def _content_disposition(filename: str) -> str:
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

    return (
        f'filename="{fallback}"; '
        f"filename*=UTF-8''{encoded}"
    )
