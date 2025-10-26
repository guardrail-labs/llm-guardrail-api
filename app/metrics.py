from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass
class _MetricHandle:
    name: str
    action: Callable[[float], None]

    def inc(self, value: float = 1.0) -> None:
        self.action(value)

    def observe(self, value: float) -> None:
        self.action(value)


class _Metric:
    def __init__(self, name: str, label_names: Iterable[str]) -> None:
        self.name = name
        self.label_names = tuple(label_names)
        self._samples: dict[tuple[str, ...], float] = defaultdict(float)

    def labels(self, **labels: str) -> _MetricHandle:
        key = tuple(labels.get(label, "") for label in self.label_names)

        def _apply(value: float) -> None:
            self._samples[key] += value

        return _MetricHandle(self.name, _apply)


class _Summary(_Metric):
    def labels(self, **labels: str) -> _MetricHandle:
        key = tuple(labels.get(label, "") for label in self.label_names)

        def _apply(value: float) -> None:
            self._samples[key] = value

        return _MetricHandle(self.name, _apply)


class MetricsRegistry:
    def counter(self, name: str, description: str, label_names: Iterable[str]) -> _Metric:
        return _Metric(name, label_names)

    def summary(self, name: str, description: str, label_names: Iterable[str]) -> _Summary:
        return _Summary(name, label_names)


_GLOBAL_REGISTRY = MetricsRegistry()


def get_registry() -> MetricsRegistry:
    return _GLOBAL_REGISTRY
