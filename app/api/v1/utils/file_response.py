from fastapi.responses import StreamingResponse

from app.core.http.content_disposition import content_disposition_inline
from app.features.storage.dto.file_download import FileDownload


def file_stream_response(download: FileDownload) -> StreamingResponse:
    headers = {
        "Content-Disposition": content_disposition_inline(
            download.file.original_filename,
        ),
        "Content-Length": str(download.file.size),
        "ETag": f'"{download.file.checksum}"',
        "Cache-Control": (
            "public, max-age=31536000, immutable"
            if download.is_public
            else "private, no-cache"
        ),
    }

    return StreamingResponse(
        download.content,
        media_type=download.file.mime_type,
        headers=headers,
    )