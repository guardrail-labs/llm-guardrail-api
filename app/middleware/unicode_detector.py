from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Iterable

from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app import settings
from app.metrics import get_registry

try:  # pragma: no cover - optional dependency
    import emoji
except Exception:  # pragma: no cover - noqa: BLE001
    emoji = None

_registry = get_registry()
unicode_detect_requests_total = _registry.counter(
    "unicode_detect_requests_total",
    "Requests analyzed by unicode detector",
    ["tenant", "path"],
)
unicode_mixed_script_total = _registry.counter(
    "unicode_mixed_script_total",
    "Requests with mixed scripts",
    ["tenant", "path"],
)
unicode_zero_width_total = _registry.counter(
    "unicode_zero_width_total",
    "Zero-width/control codepoints counted",
    ["tenant", "path"],
)
unicode_confusable_ratio = _registry.summary(
    "unicode_confusable_ratio",
    "Fraction of confusable codepoints",
    ["tenant", "path"],
)
unicode_emoji_ratio = _registry.summary(
    "unicode_emoji_ratio",
    "Fraction of emoji codepoints",
    ["tenant", "path"],
)
unicode_blocked_total = _registry.counter(
    "unicode_blocked_total",
    "Requests blocked by unicode detector",
    ["tenant", "path", "reason"],
)

_COMMON_SCRIPTS = {"Common", "Inherited"}
_LATIN = re.compile(r"[\u0000-\u024F]")
_CYRILLIC = re.compile(r"[\u0400-\u04FF]")
_GREEK = re.compile(r"[\u0370-\u03FF]")
_ARABIC = re.compile(r"[\u0600-\u06FF]")
_HEBREW = re.compile(r"[\u0590-\u05FF]")
_HANGUL = re.compile(r"[\uAC00-\uD7AF]")
_DEVANAGARI = re.compile(r"[\u0900-\u097F]")
_ZERO_WIDTH_RE = re.compile(r"[\u200B-\u200F\u202A-\u202E\u2060-\u206F\uFEFF]")
_CTRL_RE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")

_LITE_MAP = str.maketrans(
    {
        "О": "O",
        "о": "o",
        "А": "A",
        "а": "a",
        "Α": "A",
        "α": "a",
        "Ι": "I",
        "і": "i",
        "М": "M",
        "Ν": "N",
        "Ѕ": "S",
        "В": "B",
        "Ꭵ": "i",
        "０": "0",
        "１": "1",
        "２": "2",
        "３": "3",
        "４": "4",
        "５": "5",
        "６": "6",
        "７": "7",
        "８": "8",
        "９": "9",
    }
)


@dataclass
class DetectedText:
    scripts: set[str]
    confusable_count: int
    emoji_count: int
    zero_width_count: int
    total_chars: int

    @property
    def mixed_script(self) -> bool:
        return len(self.scripts - _COMMON_SCRIPTS) >= 2

    @property
    def confusable_ratio(self) -> float:
        if self.total_chars == 0:
            return 0.0
        return self.confusable_count / self.total_chars

    @property
    def emoji_ratio(self) -> float:
        if self.total_chars == 0:
            return 0.0
        return self.emoji_count / self.total_chars


def _is_emoji(ch: str) -> bool:
    if emoji is not None:  # pragma: no cover - executed when dependency present
        is_emoji = getattr(emoji, "is_emoji", None)
        if callable(is_emoji):
            return bool(is_emoji(ch))
    code = ord(ch)
    return (
        0x1F300 <= code <= 0x1FAFF
        or 0x2600 <= code <= 0x26FF
        or 0x2700 <= code <= 0x27BF
    )


def _scripts_in(text: str) -> set[str]:
    scripts: set[str] = set()
    if _LATIN.search(text):
        scripts.add("Latin")
    if _CYRILLIC.search(text):
        scripts.add("Cyrillic")
    if _GREEK.search(text):
        scripts.add("Greek")
    if _ARABIC.search(text):
        scripts.add("Arabic")
    if _HEBREW.search(text):
        scripts.add("Hebrew")
    if _HANGUL.search(text):
        scripts.add("Hangul")
    if _DEVANAGARI.search(text):
        scripts.add("Devanagari")
    return scripts


def _analyze_text(text: str) -> DetectedText:
    total = len(text)
    if total == 0:
        return DetectedText(set(), 0, 0, 0, 0)

    scripts = _scripts_in(text)
    folded = text.translate(_LITE_MAP)
    confusable_count = sum(1 for original, folded_char in zip(text, folded) if original != folded_char)
    emoji_count = sum(1 for ch in text if _is_emoji(ch))
    zero_width_count = len(_ZERO_WIDTH_RE.findall(text)) + len(_CTRL_RE.findall(text))
    return DetectedText(scripts, confusable_count, emoji_count, zero_width_count, total)


def _iter_candidate_strings(scope: Scope, body_text: str | None) -> Iterable[str]:
    headers = scope.get("headers", [])
    if settings.UNICODE_DETECT_HEADERS:
        for _, value in headers:
            try:
                yield value.decode("utf-8", "ignore")
            except Exception:  # pragma: no cover - defensive decode guard
                continue
    if settings.UNICODE_DETECT_QUERY:
        query = scope.get("query_string") or b""
        if query:
            try:
                yield query.decode("utf-8", "ignore")
            except Exception:  # pragma: no cover - defensive decode guard
                pass
    if body_text:
        yield body_text


def _get_header(headers: Iterable[tuple[bytes, bytes]], name: bytes) -> str | None:
    lowercase = name.lower()
    for key, value in headers:
        if key.lower() == lowercase:
            try:
                return value.decode("utf-8", "ignore")
            except Exception:  # pragma: no cover - defensive decode guard
                return None
    return None


def _extract_tenant(headers: Iterable[tuple[bytes, bytes]]) -> str:
    value = _get_header(headers, b"x-tenant-id")
    if value:
        return value
    return "default"


def _should_block(
    mixed_script: bool,
    confusable_ratio_value: float,
    emoji_ratio_value: float,
    zero_width_count: int,
) -> str | None:
    if settings.UNICODE_DETECT_BLOCK_MIXED_SCRIPT and mixed_script:
        return "mixed_script"
    if (
        settings.UNICODE_CONFUSABLE_RATIO_BLOCK
        and confusable_ratio_value >= settings.UNICODE_CONFUSABLE_RATIO_BLOCK
    ):
        return "confusable_ratio"
    if settings.UNICODE_EMOJI_RATIO_BLOCK and emoji_ratio_value >= settings.UNICODE_EMOJI_RATIO_BLOCK:
        return "emoji_ratio"
    if (
        settings.UNICODE_ZERO_WIDTH_COUNT_BLOCK
        and zero_width_count >= settings.UNICODE_ZERO_WIDTH_COUNT_BLOCK
    ):
        return "zero_width"
    return None


def _build_metrics_payload(
    mixed_script: bool,
    confusable_ratio_value: float,
    emoji_ratio_value: float,
    zero_width_count: int,
    scripts: set[str],
) -> dict[str, Any]:
    return {
        "mixed_script": mixed_script,
        "confusable_ratio": confusable_ratio_value,
        "emoji_ratio": emoji_ratio_value,
        "zero_width_count": zero_width_count,
        "scripts": sorted(scripts),
    }


class UnicodeDetectorMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") != "http" or not settings.UNICODE_DETECTOR_ENABLED:
            await self.app(scope, receive, send)
            return

        headers = scope.get("headers", [])
        path = scope.get("path", "")
        tenant = _extract_tenant(headers)

        body_chunks: list[Message] = []
        body_bytes = bytearray()

        while True:
            message = await receive()
            body_chunks.append(message)
            if message["type"] != "http.request":
                break
            body_bytes.extend(message.get("body", b""))
            if not message.get("more_body", False):
                break

        content_type = _get_header(headers, b"content-type")
        body_text: str | None = None
        if body_bytes and (
            content_type is None
            or "application/json" in content_type
            or content_type.startswith("text/")
        ):
            try:
                body_text = body_bytes.decode("utf-8", "ignore")
            except Exception:  # pragma: no cover - defensive decode guard
                body_text = None

        unicode_detect_requests_total.labels(tenant=tenant, path=path).inc()

        scripts_union: set[str] = set()
        confusable_total = 0
        emoji_total = 0
        zero_width_total = 0
        char_total = 0

        for candidate in _iter_candidate_strings(scope, body_text):
            detected = _analyze_text(candidate)
            scripts_union.update(detected.scripts)
            confusable_total += detected.confusable_count
            emoji_total += detected.emoji_count
            zero_width_total += detected.zero_width_count
            char_total += detected.total_chars

        mixed_script = len(scripts_union - _COMMON_SCRIPTS) >= 2
        confusable_ratio_value = (confusable_total / char_total) if char_total else 0.0
        emoji_ratio_value = (emoji_total / char_total) if char_total else 0.0

        if mixed_script:
            unicode_mixed_script_total.labels(tenant=tenant, path=path).inc()
        if zero_width_total:
            unicode_zero_width_total.labels(tenant=tenant, path=path).inc(zero_width_total)
        unicode_confusable_ratio.labels(tenant=tenant, path=path).observe(confusable_ratio_value)
        unicode_emoji_ratio.labels(tenant=tenant, path=path).observe(emoji_ratio_value)

        block_reason = _should_block(
            mixed_script,
            confusable_ratio_value,
            emoji_ratio_value,
            zero_width_total,
        )

        metrics_payload = _build_metrics_payload(
            mixed_script,
            confusable_ratio_value,
            emoji_ratio_value,
            zero_width_total,
            scripts_union,
        )

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start" and settings.UNICODE_DETECT_ANNOTATE:
                headers_list = list(message.get("headers", []))
                headers_list.append(
                    (b"x-guardrail-detect-mixed-script", b"1" if mixed_script else b"0")
                )
                headers_list.append(
                    (b"x-guardrail-confusable-ratio", str(confusable_ratio_value).encode("ascii"))
                )
                headers_list.append(
                    (b"x-guardrail-emoji-ratio", str(emoji_ratio_value).encode("ascii"))
                )
                headers_list.append(
                    (b"x-guardrail-zw-count", str(zero_width_total).encode("ascii"))
                )
                response_start: Message = dict(message)
                response_start["headers"] = headers_list
                await send(response_start)
                return
            await send(message)

        if block_reason:
            unicode_blocked_total.labels(tenant=tenant, path=path, reason=block_reason).inc()
            await send_wrapper(
                {
                    "type": "http.response.start",
                    "status": 400,
                    "headers": [(b"content-type", b"application/json")],
                }
            )
            payload = json.dumps(
                {"error": "unicode_detect_block", "reason": block_reason, "metrics": metrics_payload}
            ).encode("utf-8")
            await send({"type": "http.response.body", "body": payload, "more_body": False})
            return

        chunks_iter = iter(body_chunks)

        async def receive_replay() -> Message:
            try:
                return next(chunks_iter)
            except StopIteration:
                return {"type": "http.request", "body": b"", "more_body": False}

        await self.app(scope, receive_replay, send_wrapper)
