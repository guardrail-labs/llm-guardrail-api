from __future__ import annotations

import asyncio
import json
from typing import Any, Dict

from app import settings
from app.middleware.unicode_detector import UnicodeDetectorMiddleware
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class EchoApp:
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        assert scope["type"] == "http"
        body = bytearray()
        while True:
            message = await receive()
            if message["type"] != "http.request":
                continue
            body.extend(message.get("body", b""))
            if not message.get("more_body", False):
                break
        payload: Dict[str, Any] = {}
        if body:
            payload = json.loads(body.decode("utf-8"))
        response = {"ok": True, "payload": payload}
        headers = [(b"content-type", b"application/json")]
        await send({"type": "http.response.start", "status": 200, "headers": headers})
        await send(
            {
                "type": "http.response.body",
                "body": json.dumps(response).encode("utf-8"),
                "more_body": False,
            }
        )


def _make_app() -> ASGIApp:
    return UnicodeDetectorMiddleware(EchoApp())


def _run_request(
    app: ASGIApp,
    *,
    json_body: Dict[str, Any] | None = None,
    headers: Dict[str, str] | None = None,
    query: str = "",
) -> dict[str, Any]:
    scope: Scope = {
        "type": "http",
        "method": "POST",
        "path": "/echo",
        "headers": [],
        "query_string": query.encode("utf-8"),
    }
    prepared_headers = []
    if headers:
        prepared_headers = [
            (key.lower().encode("latin-1"), value.encode("utf-8"))
            for key, value in headers.items()
        ]
    if json_body is not None:
        prepared_headers.append((b"content-type", b"application/json"))
    scope["headers"] = prepared_headers

    body_bytes = b""
    if json_body is not None:
        body_bytes = json.dumps(json_body, ensure_ascii=False).encode("utf-8")

    response: dict[str, Any] = {"body": b"", "headers": [], "status": None}
    sent = False

    async def receive() -> Message:
        nonlocal sent
        if not sent:
            sent = True
            return {"type": "http.request", "body": body_bytes, "more_body": False}
        return {"type": "http.disconnect"}

    async def send(message: Message) -> None:
        if message["type"] == "http.response.start":
            response["status"] = message["status"]
            response["headers"] = message.get("headers", [])
        elif message["type"] == "http.response.body":
            response["body"] += message.get("body", b"")

    async def app_call() -> None:
        await app(scope, receive, send)

    asyncio.run(app_call())

    decoded_headers = {
        key.decode("latin-1"): value.decode("utf-8", "ignore")
        for key, value in response["headers"]
    }

    return {
        "status": response["status"],
        "headers": decoded_headers,
        "body": response["body"],
    }


def test_pure_latin_has_no_flags(monkeypatch: Any) -> None:
    monkeypatch.setattr(settings, "UNICODE_CONFUSABLE_RATIO_BLOCK", 0.0)
    app = _make_app()
    result = _run_request(app, json_body={"value": "paypal"})
    assert result["status"] == 200
    assert result["headers"]["x-guardrail-detect-mixed-script"] == "0"
    assert float(result["headers"]["x-guardrail-confusable-ratio"]) == 0.0
    assert float(result["headers"]["x-guardrail-emoji-ratio"]) == 0.0


def test_mixed_script_detects(monkeypatch: Any) -> None:
    monkeypatch.setattr(settings, "UNICODE_CONFUSABLE_RATIO_BLOCK", 0.0)
    app = _make_app()
    result = _run_request(app, json_body={"value": "pаypal"})
    assert result["status"] == 200
    assert result["headers"]["x-guardrail-detect-mixed-script"] == "1"
    assert float(result["headers"]["x-guardrail-confusable-ratio"]) > 0


def test_confusable_threshold_blocks(monkeypatch: Any) -> None:
    monkeypatch.setattr(settings, "UNICODE_CONFUSABLE_RATIO_BLOCK", 0.01)
    app = _make_app()
    result = _run_request(app, json_body={"value": "Αpple"})
    assert result["status"] == 400
    data = json.loads(result["body"].decode("utf-8"))
    assert data["reason"] == "confusable_ratio"
    assert data["metrics"]["confusable_ratio"] > 0.01


def test_emoji_ratio_detects(monkeypatch: Any) -> None:
    monkeypatch.setattr(settings, "UNICODE_CONFUSABLE_RATIO_BLOCK", 0.0)
    app = _make_app()
    result = _run_request(app, json_body={"value": "hello 😀😀😀"})
    assert result["status"] == 200
    assert float(result["headers"]["x-guardrail-emoji-ratio"]) > 0.05


def test_zero_width_block(monkeypatch: Any) -> None:
    monkeypatch.setattr(settings, "UNICODE_ZERO_WIDTH_COUNT_BLOCK", 3)
    app = _make_app()
    result = _run_request(app, json_body={"value": "hi\u200b\u200b\u200bthere"})
    assert result["status"] == 400
    data = json.loads(result["body"].decode("utf-8"))
    assert data["reason"] == "zero_width"
    assert data["metrics"]["zero_width_count"] >= 3


def test_header_detection_toggle(monkeypatch: Any) -> None:
    monkeypatch.setattr(settings, "UNICODE_DETECT_HEADERS", False)
    monkeypatch.setattr(settings, "UNICODE_CONFUSABLE_RATIO_BLOCK", 0.0)
    app = _make_app()
    result = _run_request(
        app,
        json_body={"value": "hello"},
        headers={"X-Custom": "pаypal"},
    )
    assert result["status"] == 200
    assert result["headers"]["x-guardrail-detect-mixed-script"] == "0"


def test_query_detection(monkeypatch: Any) -> None:
    monkeypatch.setattr(settings, "UNICODE_CONFUSABLE_RATIO_BLOCK", 0.0)
    app = _make_app()
    result = _run_request(app, json_body={"value": "plain"}, query="q=pаypal")
    assert result["status"] == 200
    assert result["headers"]["x-guardrail-detect-mixed-script"] == "1"

    monkeypatch.setattr(settings, "UNICODE_DETECT_QUERY", False)
    app_disabled = _make_app()
    result_disabled = _run_request(app_disabled, json_body={"value": "plain"}, query="q=pаypal")
    assert result_disabled["status"] == 200
    assert result_disabled["headers"]["x-guardrail-detect-mixed-script"] == "0"
