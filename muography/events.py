import numpy as np

from .config import COINC_WINDOW_FINE, FINE_UNIT_NS


def group_events(rows):
    events = {}
    for hdr, chans, adcs in rows:
        events.setdefault(hdr[1], []).append((hdr, chans, adcs))
    out = []
    for evnum in sorted(events):
        plane_rows = sorted(events[evnum], key=lambda r: r[0][5])
        times = np.array([r[0][2] for r in plane_rows], dtype=np.int64)
        span_units = int(times.max() - times.min())
        span_ns = span_units * FINE_UNIT_NS
        ok = span_units <= COINC_WINDOW_FINE
        out.append(
            {
                "event": evnum,
                "unix": plane_rows[0][0][0],
                "fine": times,
                "tdc": [(r[0][3], r[0][4]) for r in plane_rows],
                "plane_rows": plane_rows,
                "n_planes": len(plane_rows),
                "coinc_span_ns": span_ns,
                "in_window": ok,
            }
        )
    return out


def cluster_strips(chans, adcs):
    order = np.argsort(chans)
    chans = chans[order]
    adcs = adcs[order]
    clusters = []
    start = 0
    for i in range(1, len(chans) + 1):
        if i == len(chans) or chans[i] - chans[i - 1] > 1:
            c_ch = chans[start:i]
            c_ad = adcs[start:i]
            w = c_ad.astype(float)
            centroid = float(np.sum(c_ch * w) / np.sum(w))
            clusters.append(
                {
                    "size": int(i - start),
                    "centroid": centroid,
                    "strip_min": int(c_ch.min()),
                    "strip_max": int(c_ch.max()),
                    "adc_sum": float(c_ad.sum()),
                    "adc_max": float(c_ad.max()),
                }
            )
            start = i
    return clusters
