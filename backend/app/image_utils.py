from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, UnidentifiedImageError
import pillow_heif

pillow_heif.register_heif_opener()

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tiff",
    ".tif",
    ".gif",
    ".heic",
    ".heif",
}


class UnsupportedImageError(ValueError):
    pass


def validate_extension(filename: str) -> None:
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise UnsupportedImageError(
            f"Unsupported file format '{suffix}'. Supported formats: {supported}"
        )


def normalize_to_jpeg(raw_bytes: bytes) -> bytes:
    try:
        with Image.open(BytesIO(raw_bytes)) as image:
            converted = image.convert("RGB")
            output = BytesIO()
            converted.save(output, format="JPEG", quality=95)
            return output.getvalue()
    except UnidentifiedImageError as exc:
        raise UnsupportedImageError("File is not a valid image") from exc
