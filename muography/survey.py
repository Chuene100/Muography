"""Sparse underground muon-flux survey with Gaussian-process prediction.

Deploying the telescope everywhere underground is impractical, so this module
models the realistic workflow: measure the muon rate at a handful of stations
for a limited number of days each, then use Gaussian-process regression over
log-rate to predict the flux across the whole site, quantify where the model
is still uncertain, adaptively choose the next station, and finally report
the location with the fewest predicted muon hits.
"""

from pathlib import Path

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel as C

from . import physics
from .dataio import parse_paul_dat
from .events import group_events

ROCK_DENSITY_G_CM3 = 2.65

# Open-sky rate of the PAUL-style telescope (~0.41 m2 planes, cos^2 theta
# acceptance): ~170 muons/m^2/s x 0.41 m^2 x ~0.25 geometry factor.
OPEN_SKY_RATE_PER_DAY = 1.7e6


def meters_rock_to_mwe(h_m, rho=ROCK_DENSITY_G_CM3):
    return np.asarray(h_m, dtype=float) * rho


def make_site(nx=48, ny=36, extent=(0.0, 600.0, 0.0, 450.0), seed=7):
    """Synthetic site: candidate detector locations under an uneven mountain."""
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = extent
    xs = np.linspace(x0, x1, nx)
    ys = np.linspace(y0, y1, ny)
    X, Y = np.meshgrid(xs, ys)

    cx, cy = x0 + 0.62 * (x1 - x0), y0 + 0.40 * (y1 - y0)
    dome = 420.0 * np.exp(
        -(((X - cx) ** 2) / (2 * 160.0**2) + ((Y - cy) ** 2) / (2 * 130.0**2))
    )
    px, py = x0 + 0.25 * (x1 - x0), y0 + 0.75 * (y1 - y0)
    ridge = 160.0 * np.exp(-(((Y - py) ** 2) / (2 * 55.0**2)) - ((X - px) / 240.0) ** 2)

    phases = rng.uniform(0, 2 * np.pi, 6)
    freqs = rng.uniform(0.8, 2.2, 6)
    amps = rng.uniform(20.0, 55.0, 6)
    undulation = np.zeros_like(X)
    for k in range(6):
        undulation += (
            amps[k]
            * np.sin(freqs[k] * np.pi * (X - x0) / (x1 - x0) + phases[k])
            * np.cos(freqs[k] * np.pi * (Y - y0) / (y1 - y0) + phases[(k + 2) % 6])
        )

    depth_mwe = np.clip(140.0 + dome + ridge + undulation, 80.0, None)
    return {
        "xs": xs,
        "ys": ys,
        "X": X,
        "Y": Y,
        "depth_mwe": depth_mwe,
        "coords": np.column_stack([X.ravel(), Y.ravel()]),
        "extent": extent,
    }


class TransmissionCurve:
    """Integrated muon transmission vs vertical overburden in m.w.e.

    Built from the analytic model or from actual Geant4 depth-scan runs so
    that flux predictions inherit the simulated transport instead of only
    the range-energy approximation.
    """

    def __init__(self, depth_mwe, transmission, source="custom"):
        d = np.atleast_1d(np.asarray(depth_mwe, dtype=float))
        t = np.atleast_1d(np.asarray(transmission, dtype=float))
        order = np.argsort(d)
        d = np.maximum(d[order], 1.0)
        t = np.clip(t[order], 1e-12, 1.0)
        keep = np.ones(len(d), dtype=bool)
        if len(d) > 1:
            keep[1:] = d[1:] != d[:-1]
        self.depth = d[keep]
        self.transmission = np.minimum.accumulate(t[keep])
        self.source = source

    @classmethod
    def from_physics(cls, d_lo=10.0, d_hi=8000.0, n=64):
        depths = np.geomspace(d_lo, d_hi, n)
        t = np.array([physics.transmission_exact(x) for x in depths])
        return cls(depths, t, source="analytic")

    @classmethod
    def from_geant4_depth_scan(cls, sim_out_dir, anchor_analytic=True):
        """Fit transmission ratios from depth_{T}m.dat Geant4 outputs.

        All scan runs must use the same /run/beamOn so that unique-event
        counts are comparable. Depth samples that recorded zero events are
        discarded; if no depth_0 sample exists the curve is anchored to the
        analytic model at the deepest surviving point.
        """
        out_dir = Path(sim_out_dir)
        found = []
        for f in sorted(out_dir.glob("depth_*m.dat")):
            stem = f.stem[len("depth_"):-len("m")]
            if not stem.isdigit():
                continue
            rows = parse_paul_dat(f)
            found.append((int(stem), len(group_events(rows))))
        if not found:
            raise FileNotFoundError(f"no depth_*m.dat files under {out_dir}")
        found.sort()
        h_m = np.array([f[0] for f in found], dtype=float)
        counts = np.array([f[1] for f in found], dtype=float)

        usable = counts > 0
        if usable.sum() < 3:
            raise ValueError(
                f"only {int(usable.sum())} usable depth samples under {out_dir}; "
                "re-run scripts/run_depth_scan.sh with more events"
            )
        h_m, counts = h_m[usable], counts[usable]

        if h_m[0] == 0:
            ratios = counts / counts[0]
            depths = meters_rock_to_mwe(h_m)
            return cls(depths, ratios, source="geant4")
        if not anchor_analytic:
            raise ValueError("no depth_0m.dat reference run; cannot normalise")
        depths = meters_rock_to_mwe(h_m)
        ratios = counts / counts[np.argmax(depths)]
        anchor = physics.transmission_exact(float(depths.max()))
        return cls(depths, ratios * anchor, source="geant4(anchored)")

    def __call__(self, depth_mwe):
        d = np.clip(np.asarray(depth_mwe, dtype=float), self.depth[0], self.depth[-1])
        logt = np.interp(
            np.log(d), np.log(self.depth), np.log(self.transmission)
        )
        return np.exp(logt)


def true_rate_map(site, transmission, r_ref_per_day):
    """Muon rate per day at every grid cell for the true depth field."""
    return r_ref_per_day * transmission(site["depth_mwe"])


def simulate_station(coords_xy, rate_per_day, days, rng):
    """One detector deployment: Poisson counts over the exposure time."""
    counts = int(rng.poisson(np.asarray(rate_per_day, dtype=float) * days))
    rate_hat = (counts + 0.5) / days
    rate_sigma = np.sqrt(counts + 0.5) / days
    return {
        "x": float(coords_xy[0]),
        "y": float(coords_xy[1]),
        "counts": counts,
        "days": float(days),
        "rate_per_day_hat": float(rate_hat),
        "rate_per_day_sigma": float(rate_sigma),
    }


def fit_flux_gp(stations, length_scale_m=90.0, seed=42):
    """Gaussian-process regression of log10(muon rate) over station coords."""
    xy = np.array([[s["x"], s["y"]] for s in stations])
    y = np.log10([s["rate_per_day_hat"] for s in stations])
    sig = np.array(
        [s["rate_per_day_sigma"] / (np.log(10) * s["rate_per_day_hat"]) for s in stations]
    )
    kernel = C(1.0, (1e-3, 1e3)) * Matern(
        length_scale=length_scale_m, length_scale_bounds=(25.0, 1500.0), nu=1.5
    ) + WhiteKernel(1e-3, (1e-7, 1e-1))
    gp = GaussianProcessRegressor(
        kernel=kernel,
        alpha=sig**2,
        normalize_y=True,
        n_restarts_optimizer=4,
        random_state=seed,
    )
    gp.fit(xy, y)
    return gp


def predict_flux_map(gp, site):
    """Predicted log10-rate mean and std over the whole site grid."""
    mean, std = gp.predict(site["coords"], return_std=True)
    shape = site["depth_mwe"].shape
    return mean.reshape(shape), std.reshape(shape)


def locate_minimum(mean_log_rate, site):
    """Grid location with the fewest predicted muon hits."""
    idx = int(np.argmin(mean_log_rate))
    x, y = site["coords"][idx]
    return {"index": idx, "x": float(x), "y": float(y),
            "log10_rate": float(mean_log_rate.ravel()[idx])}


def pick_next_station(gp, site, stations, min_separation_m=40.0):
    """Active learning: unmeasured grid point with maximal model uncertainty,
    kept at least `min_separation_m` away from existing deployments."""
    _, std = predict_flux_map(gp, site)
    flat_idx = np.argsort(std.ravel())[::-1]
    measured = np.array([[s["x"], s["y"]] for s in stations]) if stations else None
    for idx in flat_idx:
        cand = site["coords"][idx]
        if measured is not None and np.min(np.hypot(measured[:, 0] - cand[0],
                                                    measured[:, 1] - cand[1])) < min_separation_m:
            continue
        return {"index": int(idx), "x": float(cand[0]), "y": float(cand[1]),
                "std": float(std.ravel()[idx])}
    raise RuntimeError("no candidate location satisfies the separation constraint")


def run_adaptive_survey(site, true_rates, transmission, n_start=6, n_total=14,
                        days_per_station=3.0, r_ref_per_day=OPEN_SKY_RATE_PER_DAY,
                        seed=11, length_scale_m=90.0):
    """Deploy sparsely, adaptively refine, and localise the flux minimum.

    Returns the fitted GP, predicted maps and a per-step history comparing
    the predicted minimum against the true one.
    """
    if true_rates is None:
        true_rates = true_rate_map(site, transmission, r_ref_per_day)
    rng = np.random.default_rng(seed)
    rates_flat = true_rates.ravel()
    n_cells = len(rates_flat)

    chosen = list(rng.choice(n_cells, size=n_start, replace=False))
    history = []

    while True:
        stations = [
            simulate_station(site["coords"][i], rates_flat[i], days_per_station, rng)
            for i in chosen
        ]
        gp = fit_flux_gp(stations, length_scale_m=length_scale_m, seed=seed)
        mean_log, std_log = predict_flux_map(gp, site)
        pred_min = locate_minimum(mean_log, site)
        true_idx = int(np.argmin(rates_flat))
        tx, ty = site["coords"][true_idx]
        err_m = float(np.hypot(pred_min["x"] - tx, pred_min["y"] - ty))
        history.append({
            "n_stations": len(stations),
            "predicted_min": pred_min,
            "true_min": {"index": true_idx, "x": float(tx), "y": float(ty)},
            "location_error_m": err_m,
            "mean_uncertainty": float(np.mean(std_log)),
        })
        if len(chosen) >= n_total:
            break
        nxt = pick_next_station(gp, site, stations)
        chosen.append(nxt["index"])

    return {
        "gp": gp,
        "stations": stations,
        "chosen_indices": chosen,
        "mean_log_rate": mean_log,
        "std_log_rate": std_log,
        "history": history,
        "true_rates": true_rates,
        "true_min_index": true_idx,
    }
