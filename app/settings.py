from __future__ import annotations

import os

__all__ = [
    "bool_env",
    "int_env",
    "float_env",
    "UNICODE_DETECTOR_ENABLED",
    "UNICODE_DETECT_HEADERS",
    "UNICODE_DETECT_QUERY",
    "UNICODE_DETECT_BLOCK_MIXED_SCRIPT",
    "UNICODE_CONFUSABLE_RATIO_BLOCK",
    "UNICODE_EMOJI_RATIO_BLOCK",
    "UNICODE_ZERO_WIDTH_COUNT_BLOCK",
    "UNICODE_DETECT_ANNOTATE",
]

_TRUE_VALUES = {"1", "true", "t", "yes", "y", "on"}
_FALSE_VALUES = {"0", "false", "f", "no", "n", "off"}


def _normalize_env(value: str | None) -> str | None:
    if value is None:
        return None
    return value.strip()


def bool_env(key: str, default: bool = False) -> bool:
    value = _normalize_env(os.getenv(key))
    if value is None:
        return default
    lowered = value.lower()
    if lowered in _TRUE_VALUES:
        return True
    if lowered in _FALSE_VALUES:
        return False
    return default


def int_env(key: str, default: int = 0) -> int:
    value = _normalize_env(os.getenv(key))
    if value is None:
        return default
    try:
        return int(value, 0)
    except ValueError:
        return default


def float_env(key: str, default: float = 0.0) -> float:
    value = _normalize_env(os.getenv(key))
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


# --- Unicode Detector v1.1 ---
UNICODE_DETECTOR_ENABLED = bool_env("UNICODE_DETECTOR_ENABLED", True)
# Trigger detection on request headers/body/query (read-only analysis)
UNICODE_DETECT_HEADERS = bool_env("UNICODE_DETECT_HEADERS", True)
UNICODE_DETECT_QUERY = bool_env("UNICODE_DETECT_QUERY", True)

# Thresholds (0 disables blocking)
UNICODE_DETECT_BLOCK_MIXED_SCRIPT = bool_env("UNICODE_DETECT_BLOCK_MIXED_SCRIPT", False)
UNICODE_CONFUSABLE_RATIO_BLOCK = float_env("UNICODE_CONFUSABLE_RATIO_BLOCK", 0.0)
UNICODE_EMOJI_RATIO_BLOCK = float_env("UNICODE_EMOJI_RATIO_BLOCK", 0.0)
UNICODE_ZERO_WIDTH_COUNT_BLOCK = int_env("UNICODE_ZERO_WIDTH_COUNT_BLOCK", 0)

# Annotation/return behavior
UNICODE_DETECT_ANNOTATE = bool_env("UNICODE_DETECT_ANNOTATE", True)
