import numpy as np

from .events import cluster_strips
from .tracking import reconstruct_track


def event_features(event):
    feats = {
        "event": event["event"],
        "n_planes": event["n_planes"],
        "coinc_span_ns": event["coinc_span_ns"],
    }
    total_hits = 0
    total_adc = 0.0
    max_adc = 0.0
    n_clusters = 0
    max_cluster_size = 0
    adc_per_plane = []
    hits_per_plane = []
    clusters_per_plane = []
    for hdr, chans, adcs in event["plane_rows"]:
        chans = np.asarray(chans)
        adcs = np.asarray(adcs)
        cl = cluster_strips(chans, adcs)
        n_clusters += len(cl)
        max_cluster_size = max(max_cluster_size, max(c["size"] for c in cl))
        total_hits += len(chans)
        total_adc += float(adcs.sum())
        max_adc = max(max_adc, float(adcs.max()))
        adc_per_plane.append(float(adcs.sum()))
        hits_per_plane.append(len(chans))
        clusters_per_plane.append(len(cl))
    trk = reconstruct_track(event)
    if trk is not None:
        feats.update(
            theta_deg=trk["theta_deg"],
            phi_deg=trk["phi_deg"],
            y_res_mm=abs(trk["y_res_mm"]),
            dx_dz=trk["dx_dz"],
            dy_dz=trk["dy_dz"],
        )
    else:
        feats.update(theta_deg=np.nan, phi_deg=np.nan, y_res_mm=np.nan,
                     dx_dz=np.nan, dy_dz=np.nan)
    feats.update(
        total_hits=total_hits,
        total_adc=total_adc,
        max_adc=max_adc,
        mean_hits_per_plane=total_hits / max(len(event["plane_rows"]), 1),
        n_clusters=n_clusters,
        max_cluster_size=max_cluster_size,
        adc_spread=float(np.std(adc_per_plane)),
        min_hits_plane=min(hits_per_plane) if hits_per_plane else 0,
    )
    return feats


def feature_matrix(feature_dicts):
    keys = [
        "n_planes", "coinc_span_ns", "total_hits", "mean_hits_per_plane",
        "total_adc", "max_adc", "n_clusters", "max_cluster_size",
        "adc_spread", "min_hits_plane", "theta_deg", "phi_deg", "y_res_mm",
    ]
    X = np.array(
        [[f[k] if f.get(k) == f.get(k) else -1.0 for k in keys] for f in feature_dicts],
        dtype=float,
    )
    return X, keys


def clean_muon_mask(feature_dicts):
    out = []
    for f in feature_dicts:
        ok = (
            f["n_planes"] == 3
            and f["coinc_span_ns"] <= 200.0
            and f["max_cluster_size"] <= 3
            and f["theta_deg"] < 80.0
            and f["total_hits"] <= 20
        )
        out.append(ok)
    return np.array(out, dtype=bool)


def synthesize_noise_events(rows, rng, n_out):
    import copy

    idx = rng.integers(0, len(rows), size=(n_out, 3))
    out = []
    for k in range(n_out):
        ev = []
        tdc = (int(rng.integers(5, 15)), int(rng.integers(6, 18)))
        base_unix = rows[idx[k, 0]][0][0]
        base_evt = int(k)
        for j, src_idx in enumerate(idx[k]):
            hdr, chans, adcs = rows[src_idx]
            chans = chans.copy()
            adcs = adcs.copy()
            roll = int(rng.integers(-20, 21))
            chans = ((chans + roll) % 64).astype(chans.dtype)
            keep = rng.random(len(chans)) > 0.25
            chans, adcs = chans[keep], adcs[keep]
            if len(chans) < 2:
                pad = rng.choice(64, size=2, replace=False)
                chans = np.concatenate([chans, pad])
                adcs = np.concatenate([adcs, rng.integers(10, 4000, size=2)])
            plane = j
            fine = int(hdr[2] + int(rng.integers(-5000, 5001)))
            new_hdr = np.array([base_unix, base_evt, fine % int(1e8),
                                tdc[0], tdc[1], plane, 0, 0, len(chans)])
            ev.append((new_hdr, chans, adcs))
        out.append(ev)
    return out
