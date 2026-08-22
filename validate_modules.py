import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from muography import config as C
from muography import dataio, features, rates, tracking
from muography.events import cluster_strips, group_events

PASS = []
FAIL = []


def check(name, cond, info=""):
    (PASS if cond else FAIL).append((name, info))
    print(f"  {'PASS' if cond else 'FAIL'}  {name} {info}")


def make_row(unix, evt, fine, plane, chans, adcs, tdc=(10, 12)):
    hdr = np.array([unix, evt, fine, tdc[0], tdc[1], plane, 0, 0,
                    len(chans)], dtype=np.int64)
    inter = []
    for c_, a_ in zip(chans, adcs):
        inter.extend([int(c_), int(a_)])
    return hdr, np.array(chans, dtype=np.int64), np.array(adcs, dtype=np.int64)


print("[1] parser")
tmp = Path("/tmp/paul_test.dat")
lines = []
lines.append("1700000000 0 100 10 12 0 0 0 2 5 100 6 200")
lines.append("1700000000 0 101 10 12 1 0 0 3 7 300 8 400 9 500")
lines.append("1700000000 0 102 10 12 2 0 0 2 10 600 11 700")
lines.append("1700000000 1 900 10 12 0 0 0 4 1 50")
lines.append("1700000000 1 905 10 12 1 0 0 64 " + " ".join(
    f"{i} {10 * i}" for i in range(64)))
tmp.write_text("\n".join(lines) + "\n")
rows = dataio.parse_paul_dat(tmp)
check("row count", len(rows) == 5)
q = dataio.data_quality(rows)
check("nhits mismatch detected", q["rows_with_nhits_mismatch"] == 1)
r = rows[0]
check("pairs parsed", len(r[1]) == 2 and r[1].tolist() == [5, 6])
r_trunc = rows[3]
check("truncated row -> min pairs", len(r_trunc[1]) == 1)
r_full = rows[4]
check("full 64-strip row", len(r_full[1]) == 64)

print("[2] clustering")
cl = cluster_strips(np.array([3, 4, 5, 20, 22]), np.array([100, 400, 100, 90, 80]))
check("adjacent merged into one cluster", len(cl) == 3)
check("adc-weighted centroid", abs(cl[0]["centroid"] - 4.0) < 1e-9)
check("cluster sizes", cl[0]["size"] == 3 and cl[1]["size"] == 1)

print("[3] event builder")
evs = group_events(rows[:3])
check("one event", len(evs) == 1 and evs[0]["n_planes"] == 3)
check("coinc window ok", evs[0]["in_window"])
e_far = group_events([rows[0], rows[1], make_row(1700000000, 0, 100 + 25, 2, [1, 2], [10, 10])])
check("outside 200 ns flagged", e_far[0]["in_window"] is False and e_far[0]["coinc_span_ns"] == 250.0)

print("[4] tracking with known track")
spacing = C.PLANE_SPACING_MM
dx_dz_true, dy_dz_true = 0.30, -0.40
x0_mm = -60.0
y1_mm = dy_dz_true * spacing
x2_mm = x0_mm + dx_dz_true * 2 * spacing


def strip_of(mm):
    return int(round(mm / C.STRIP_PITCH_MM + (C.N_STRIPS - 1) / 2))


ev_rows = [
    make_row(1700000001, 7, 500, 0, [strip_of(x0_mm)], [1000]),
    make_row(1700000001, 7, 505, 1, [strip_of(y1_mm)], [1000]),
    make_row(1700000001, 7, 510, 2, [strip_of(x2_mm)], [1000]),
]
trk = tracking.reconstruct_track(group_events(ev_rows)[0])
import math
theta_true = math.degrees(math.atan(math.hypot(dx_dz_true, dy_dz_true)))
phi_true = math.degrees(math.atan2(dy_dz_true, dx_dz_true))
check(f"theta {trk['theta_deg']:.2f} ~ {theta_true:.2f}",
      abs(trk["theta_deg"] - theta_true) < 1.5)
check(f"phi {trk['phi_deg']:.2f} ~ {phi_true:.2f}",
      abs(trk["phi_deg"] - phi_true) < 1.5)
check("vertical track -> theta~0",
      tracking.reconstruct_track(
          group_events([
              make_row(1700000002, 8, 100, 0, [31, 32], [500, 500]),
              make_row(1700000002, 8, 105, 1, [31, 32], [500, 500]),
              make_row(1700000002, 8, 110, 2, [31, 32], [500, 500]),
          ])[0]
      )["theta_deg"] < 1.0)

print("[5] real-data smoke test")
real = dataio.parse_paul_dat(C.DATA_FILE)
real_evs = group_events(real)
rl = rates.live_time_and_rates(real_evs)
spans = np.array([e["coinc_span_ns"] for e in real_evs])
thetas, phis = [], []
for e in real_evs:
    t = tracking.reconstruct_track(e)
    if t:
        thetas.append(t["theta_deg"])
        phis.append(t["phi_deg"])
thetas = np.array(thetas)
phis = np.array(phis)
check(f"{len(real)} rows parsed", len(real) == 25260)
check(f"{len(real_evs)} events", len(real_evs) == 8420)
check(f"rate {rl['rate_hz']:.2f} Hz", 13.5 < rl["rate_hz"] < 14.5)
check(f"all spans <= 150 ns (max {spans.max():.0f})", spans.max() <= 150)
check(f"tracks reconstructed for all events ({len(thetas)})", len(thetas) == len(real_evs))
check(f"theta bounded by geometry (<65 deg, max {thetas.max():.1f})", thetas.max() < 65.0)
check("phi covers full circle", phis.max() - phis.min() > 350)
fmat = [features.event_features(e) for e in real_evs]
clean = features.clean_muon_mask(fmat)
check(f"clean fraction {clean.mean():.2f}", 0.7 < clean.mean() <= 1.0)

print()
if FAIL:
    print(f"RESULT: {len(FAIL)} FAILED / {len(PASS)} passed")
    sys.exit(1)
print(f"RESULT: ALL {len(PASS)} CHECKS PASSED")
