import numpy as np

from .config import FINE_UNIT_NS


def live_time_and_rates(events):
    times = np.array([e["unix"] for e in events], dtype=np.float64)
    t0 = times.min()
    t1 = times.max()
    span_s = max(t1 - t0, 1.0)
    rate_hz = len(events) / span_s
    return {
        "t_start": t0,
        "t_end": t1,
        "span_s": span_s,
        "span_h": span_s / 3600.0,
        "n_events": len(events),
        "rate_hz": rate_hz,
        "rate_per_hour": rate_hz * 3600.0,
        "rate_per_day": rate_hz * 86400.0,
    }


def hourly_series(events):
    times = np.array([e["unix"] for e in events], dtype=np.int64)
    t0 = times.min()
    hours = ((times - t0) // 3600).astype(int)
    bins = np.arange(0, hours.max() + 2)
    counts, _ = np.histogram(hours, bins=bins - 0.5)
    centers = (bins[:-1] + bins[1:]) / 2.0
    return centers, counts


def fine_time_residuals(events):
    res = []
    for e in events:
        f = e["fine"].astype(np.int64)
        if len(f) >= 3:
            res.append(f.max() - f.min())
    return np.array(res) * FINE_UNIT_NS
