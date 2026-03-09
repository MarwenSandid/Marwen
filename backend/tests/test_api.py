from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def make_image(fmt: str = "PNG") -> bytes:
    img = Image.new("RGB", (10, 10), color="red")
    out = BytesIO()
    img.save(out, format=fmt)
    return out.getvalue()


def test_health() -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_analyze_valid_image_returns_schema() -> None:
    files = {"file": ("car.png", make_image("PNG"), "image/png")}
    res = client.post("/analyze", files=files)
    assert res.status_code == 200
    body = res.json()
    assert set(body.keys()) == {
        "make",
        "model",
        "production_date",
        "country_of_origin",
        "confidence",
        "notes",
    }


def test_analyze_rejects_unsupported_extension() -> None:
    files = {"file": ("car.txt", b"nope", "text/plain")}
    res = client.post("/analyze", files=files)
    assert res.status_code == 415
