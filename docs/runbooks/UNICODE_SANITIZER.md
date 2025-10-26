# Unicode Sanitizer Runbook

The Unicode sanitizer and detector protect the Guardrail API from spoofed or visually
confusing payloads. Sanitization continues to normalize content while the detector provides
telemetry and optional blocking to flag suspicious input before it is normalized.

## Detector v1.1 (Telemetry & Blocking)

Detector v1.1 introduces read-only analysis across request headers, query parameters, and
request bodies. It records suspicious patterns, emits Prometheus metrics, and can optionally
block offending requests.

### Settings

All settings are available as environment variables and default to a detect-only posture.

| Variable | Default | Description |
| --- | --- | --- |
| `UNICODE_DETECTOR_ENABLED` | `true` | Enables the Unicode detector middleware. |
| `UNICODE_DETECT_HEADERS` | `true` | Analyze incoming request headers. |
| `UNICODE_DETECT_QUERY` | `true` | Analyze the query string (raw UTF-8). |
| `UNICODE_DETECT_BLOCK_MIXED_SCRIPT` | `false` | Block when multiple scripts appear (excluding Common/Inherited). |
| `UNICODE_CONFUSABLE_RATIO_BLOCK` | `0.0` | Block when the confusable ratio meets/exceeds the threshold. |
| `UNICODE_EMOJI_RATIO_BLOCK` | `0.0` | Block when emoji ratio meets/exceeds the threshold. |
| `UNICODE_ZERO_WIDTH_COUNT_BLOCK` | `0` | Block when zero-width/control count meets/exceeds the threshold. |
| `UNICODE_DETECT_ANNOTATE` | `true` | Emit response headers with detector annotations. |

### Metrics

The detector exports per-tenant metrics with the request path as a secondary label. All
metrics are emitted even when blocking is disabled.

| Metric | Type | Labels | Notes |
| --- | --- | --- | --- |
| `unicode_detect_requests_total` | Counter | `tenant`, `path` | Requests inspected. |
| `unicode_mixed_script_total` | Counter | `tenant`, `path` | Mixed-script detections. |
| `unicode_confusable_ratio` | Summary | `tenant`, `path` | Observed confusable ratio (0–1). |
| `unicode_emoji_ratio` | Summary | `tenant`, `path` | Observed emoji ratio (0–1). |
| `unicode_zero_width_total` | Counter | `tenant`, `path` | Zero-width or bidi control characters counted. |
| `unicode_blocked_total` | Counter | `tenant`, `path`, `reason` | Requests blocked by the detector. |

The middleware adds the following headers to every HTTP response when
`UNICODE_DETECT_ANNOTATE=true`:

* `X-Guardrail-Detect-Mixed-Script`
* `X-Guardrail-Confusable-Ratio`
* `X-Guardrail-Emoji-Ratio`
* `X-Guardrail-ZW-Count`

### Alerts

Prometheus rules are appended to `deploy/monitoring/prometheus/guardrail_rules.yml`:

```
- alert: GuardrailUnicodeMixedScriptSpike
  expr: sum(rate(unicode_mixed_script_total[10m])) by (tenant) > 5
  for: 10m
  labels: { severity: warning }
  annotations:
    summary: "Mixed-script detections spiking for {{ $labels.tenant }}"
    description: "Potential homoglyph phishing/spoof attempts."

- alert: GuardrailUnicodeConfusableHigh
  expr: avg_over_time(unicode_confusable_ratio[15m]) by (tenant) > 0.08
  for: 15m
  labels: { severity: warning }
  annotations:
    summary: "High confusable ratio"
    description: "Confusables > 8% on average over 15m."

- alert: GuardrailUnicodeZeroWidthBurst
  expr: sum(rate(unicode_zero_width_total[5m])) by (tenant) > 50
  for: 10m
  labels: { severity: info }
  annotations:
    summary: "Zero-width characters burst"
    description: "Spike of zero-widths (hidden text / bidi control attempts)."
```

### Grafana Dashboard

Import `deploy/monitoring/grafana/dashboards/guardrail_unicode_v1.json` to view detector
telemetry. The dashboard includes:

* Confusable ratio and emoji ratio time-series panels (per tenant).
* Mixed-script detection rate bar gauge (5-minute rate).
* Blocked-request stat split by tenant and reason (1-hour lookback).
* Table of top paths by confusable ratio.

### Rollout Guidance

1. Ship with default settings (detection only, `UNICODE_*_BLOCK=0`).
2. Monitor Grafana panels for confusable and emoji ratios; adjust thresholds based on tenant
   baseline.
3. When ready to enforce:
   * Enable `UNICODE_CONFUSABLE_RATIO_BLOCK=0.08` for suspicious tenants.
   * Set `UNICODE_ZERO_WIDTH_COUNT_BLOCK=8` for heavy zero-width misuse.
   * Toggle `UNICODE_DETECT_BLOCK_MIXED_SCRIPT=1` for high-risk tenants subject to spoofing.
4. Investigate spikes via Prometheus alerts and the dashboard; drill down on the `path` label
   to identify offending endpoints.

Blocking responses include a JSON payload describing the triggering reason and raw metrics to
assist with incident response.
