import numpy as np

from .config import N_STRIPS, PLANE_SPACING_MM, PLANE_VIEW, STRIP_PITCH_MM
from .events import cluster_strips


def plane_track_point(chans, adcs):
    cl = cluster_strips(chans.astype(np.int64), adcs.astype(np.int64))
    if not cl:
        return None
    best = max(cl, key=lambda c: c["adc_sum"])
    return best["centroid"] - (N_STRIPS - 1) / 2.0


def reconstruct_track(event):
    by_plane = {}
    used_clusters = {}
    for hdr, chans, adcs in event["plane_rows"]:
        p = int(hdr[5])
        cl = cluster_strips(chans.astype(np.int64), adcs.astype(np.int64))
        if not cl:
            continue
        best = max(cl, key=lambda c: c["adc_sum"])
        by_plane[p] = best["centroid"] - (N_STRIPS - 1) / 2.0
        used_clusters[p] = best
    if not {0, 1, 2} <= set(by_plane):
        return None
    x0 = by_plane[0] * STRIP_PITCH_MM
    y1 = by_plane[1] * STRIP_PITCH_MM
    x2 = by_plane[2] * STRIP_PITCH_MM
    z = [0.0, PLANE_SPACING_MM, 2.0 * PLANE_SPACING_MM]
    dx_dz = (x2 - x0) / (z[2] - z[0])
    dy_dz = y1 / z[1]
    tan_theta = float(np.hypot(dx_dz, dy_dz))
    theta = float(np.degrees(np.arctan(tan_theta)))
    phi = float(np.degrees(np.arctan2(dy_dz, dx_dz)))
    x_mid_pred = x0 + dx_dz * z[1]
    y_res = y1 - x_mid_pred
    return {
        "x_top": x0,
        "x_bot": x2,
        "y_mid": y1,
        "hit_mm": {
            "p0_x_mm": x0,
            "p1_y_mm": y1,
            "p2_x_mm": x2,
        },
        "cluster_sizes": {p: used_clusters[p]["size"] for p in used_clusters},
        "dx_dz": float(dx_dz),
        "dy_dz": float(dy_dz),
        "theta_deg": theta,
        "phi_deg": phi,
        "y_res_mm": y_res * STRIP_PITCH_MM,
        "views": [PLANE_VIEW[p] for p in sorted(by_plane)],
    }
