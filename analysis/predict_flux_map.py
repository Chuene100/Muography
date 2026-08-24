"""End-to-end flux-minimum prediction: Geant4-calibrated transmission,
sparse adaptive survey, Gaussian-process flux map, and localisation of the
site with the fewest muon hits.

Run inside the container as the last pipeline stage, or locally:
    python3 analysis/predict_flux_map.py [--skip-geant4]
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from muography import config as C
from muography import survey


def load_transmission(sim_out_dir):
    try:
        curve = survey.TransmissionCurve.from_geant4_depth_scan(sim_out_dir)
        print(f"Transmission curve trained on Geant4 depth scan ({curve.source})")
        print(f"  sampled depths (m.w.e.): {np.round(curve.depth, 1).tolist()}")
    except (FileNotFoundError, ValueError) as exc:
        curve = survey.TransmissionCurve.from_physics()
        print(f"Geant4 depth scan unusable ({exc}); using analytic transmission")
    return curve


def main():
    C.FIG_DIR.mkdir(parents=True, exist_ok=True)
    C.RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    curve = load_transmission(C.SIM_OPEN_SKY.parent)

    site = survey.make_site()
    r_ref = survey.OPEN_SKY_RATE_PER_DAY
    true_rates = survey.true_rate_map(site, curve, r_ref)
    true_idx = int(np.argmin(true_rates))
    tx, ty = site["coords"][true_idx]
    print(
        f"Site: {site['depth_mwe'].shape[0]}x{site['depth_mwe'].shape[1]} cells, "
        f"depth {site['depth_mwe'].min():.0f}-{site['depth_mwe'].max():.0f} m.w.e."
    )
    print(f"True flux minimum at ({tx:.1f}, {ty:.1f}) m: "
          f"{true_rates.ravel()[true_idx]:.4g} muons/day")

    result = survey.run_adaptive_survey(site, true_rates, curve, seed=11)

    mean_log = result["mean_log_rate"]
    std_log = result["std_log_rate"]
    stations = result["stations"]

    fig, axes = plt.subplots(2, 3, figsize=(18, 9))
    ext = [site["extent"][0], site["extent"][1], site["extent"][2], site["extent"][3]]

    ax = axes[0, 0]
    im = ax.imshow(site["depth_mwe"], origin="lower", extent=ext, cmap="terrain")
    ax.set_title("Overburden depth (m.w.e.)")
    fig.colorbar(im, ax=ax)

    ax = axes[0, 1]
    im = ax.imshow(np.log10(true_rates), origin="lower", extent=ext, cmap="viridis")
    ax.plot(tx, ty, "w*", ms=18, mec="k", label="true minimum")
    ax.set_title(r"True rate  $\log_{10}(muons/day)$")
    fig.colorbar(im, ax=ax)
    ax.legend(loc="upper right", fontsize=8)

    ax = axes[0, 2]
    im = ax.imshow(mean_log, origin="lower", extent=ext, cmap="viridis",
                   vmin=np.log10(true_rates.min()), vmax=np.log10(true_rates.max()))
    sx = [s["x"] for s in stations]
    sy = [s["y"] for s in stations]
    ax.scatter(sx, sy, c="r", marker="v", s=60, edgecolors="k",
               label=f"{len(stations)} stations ({result['history'][-1]['n_stations']} used)")
    pm = result["history"][-1]["predicted_min"]
    ax.plot(pm["x"], pm["y"], "r*", ms=18, mec="k", label="ML predicted minimum")
    ax.plot(tx, ty, "w*", ms=18, mec="k", label="true minimum")
    ax.set_title("GP predicted rate map")
    fig.colorbar(im, ax=ax)
    ax.legend(loc="upper right", fontsize=8)

    ax = axes[1, 0]
    im = ax.imshow(std_log, origin="lower", extent=ext, cmap="magma")
    ax.scatter(sx, sy, c="c", marker="v", s=60, edgecolors="k")
    ax.set_title("GP uncertainty (log-rate)")
    fig.colorbar(im, ax=ax)

    ax = axes[1, 1]
    ns = [h["n_stations"] for h in result["history"]]
    errs = [h["location_error_m"] for h in result["history"]]
    ax.plot(ns, errs, "o-", color="tab:blue")
    ax.axhline(0.0, color="k", lw=0.8, ls="--")
    ax.set_xlabel("number of deployed stations")
    ax.set_ylabel("|predicted - true| minimum distance (m)")
    ax.set_title("Adaptive survey convergence")

    ax = axes[1, 2]
    pred_rates = 10 ** mean_log
    ax.scatter(true_rates, pred_rates, s=4, alpha=0.3)
    lims = [true_rates.min(), true_rates.max()]
    ax.plot(lims, lims, "k--", lw=0.8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("true rate (muons/day)")
    ax.set_ylabel("GP predicted rate (muons/day)")
    ax.set_title("Predicted vs truth over all cells")

    fig.suptitle(
        "Muon-flux mapping: sparse detector deployments -> GP prediction of the "
        "minimum-flux location"
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out_png = C.FIG_DIR / "flux_map_prediction.png"
    fig.savefig(out_png, dpi=150)
    plt.close(fig)
    print(f"Figure written to {out_png}")

    last = result["history"][-1]
    summary = {
        "transmission_source": curve.source,
        "transmission_depths_mwe": curve.depth.tolist(),
        "transmission_values": curve.transmission.tolist(),
        "open_sky_rate_per_day": r_ref,
        "n_stations_final": len(stations),
        "days_per_station": result["stations"][0]["days"],
        "stations": [
            {k: v for k, v in s.items()} for s in stations
        ],
        "predicted_minimum": last["predicted_min"],
        "true_minimum": last["true_min"],
        "final_location_error_m": last["location_error_m"],
        "convergence_history": result["history"],
        "gp_kernel": str(result["gp"].kernel_),
    }
    #out_json = C.RESULTS_DIR / "flux_prediction.json"
    #out_json.write_text(json.dumps(summary, indent=2))
    #print(f"Summary written to {out_json}")
    #print(
    #    f"Final ML-predicted minimum: ({last['predicted_min']['x']:.1f}, "
    #    f"{last['predicted_min']['y']:.1f}) m, error {last['location_error_m']:.1f} m"
    #)

    out_json = C.RESULTS_DIR / "flux_prediction.json"
    
    try:
        out_json.write_text(json.dumps(summary, indent=2))
    except TimeoutError:
        # Fallback if iCloud locks the file system: force write via standard atomic I/O
        with open(out_json, "w", encoding="utf-8") as f:
            f.write(json.dumps(summary, indent=2))

    print(f"Summary written to {out_json}")
    print(
        f"Final ML-predicted minimum: ({last['predicted_min']['x']:.1f}, "
        f"{last['predicted_min']['y']:.1f}) m, error {last['location_error_m']:.1f} m"
    )



if __name__ == "__main__":
    main()
