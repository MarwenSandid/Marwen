from fastapi import FastAPI, File, HTTPException, UploadFile

from .image_utils import UnsupportedImageError, normalize_to_jpeg, validate_extension
from .providers import build_provider
from .schemas import CarAnalysis

app = FastAPI(title="Car Identifier API", version="0.1.0")
provider = build_provider()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=CarAnalysis)
async def analyze_car(file: UploadFile = File(...)) -> CarAnalysis:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    try:
        validate_extension(file.filename)
        raw_bytes = await file.read()
        normalized = normalize_to_jpeg(raw_bytes)
        return provider.analyze(normalized)
    except UnsupportedImageError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Inference error: {exc}") from exc
