# Car Identification App (iOS + Android)

This repository provides a production-ready starter for a mobile app that:

1. Accepts a car photo from gallery/camera formats (`jpg`, `png`, `webp`, `heic`, `bmp`, `tiff`, etc.).
2. Sends the image to a backend inference API.
3. Returns:
   - Make
   - Model
   - Production date (best estimate)
   - Country of origin

## Architecture

- `mobile/`: Expo React Native app for iOS and Android.
- `backend/`: FastAPI service that validates and normalizes input image formats, then runs vision inference.

## Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Optional real AI model

By default the backend uses a mock provider. To enable real inference:

```bash
export OPENAI_API_KEY=your_key_here
```

Then restart the backend.

## Mobile setup

```bash
cd mobile
npm install
npm run start
```

- Android emulator should use `http://10.0.2.2:8000` to reach host machine.
- For iOS simulator/device, update `API_BASE_URL` in `mobile/App.tsx` to your LAN IP.

## API contract

`POST /analyze` with multipart file field `file`.

Response shape:

```json
{
  "make": "Toyota",
  "model": "Corolla",
  "production_date": "2019",
  "country_of_origin": "Japan",
  "confidence": 0.87,
  "notes": "Estimated from front grille and badge"
}
```

## Notes on "all possible formats"

No system can truly support every binary format, but this implementation supports the common image families used by mobile devices and social apps, including HEIC from iPhones. Unsupported or corrupted files receive a clear `415` error.
