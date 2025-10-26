from __future__ import annotations

from fastapi import FastAPI

from app import settings
from app.middleware.unicode_detector import UnicodeDetectorMiddleware

app = FastAPI()

if settings.UNICODE_DETECTOR_ENABLED:
    app.add_middleware(UnicodeDetectorMiddleware)
