import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from muography import config as C
from muography import dataio, features, ml_models, physics, rates, tracking
from muography.events import cluster_strips, group_events


def main():
    C.FIG_DIR.mkdir(parents=True, exist_ok=True)
    C.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    C.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    results = {}

    rows = dataio.parse_paul_dat(C.DATA_FILE)
    print(f"Parsed {len(rows)} plane rows from {C.DATA_FILE.name}")

    events = group_events(rows)
    print(f"Built {len(events)} events")

    rl = rates.live_time_and_rates(events)
    start_utc = datetime.fromtimestamp(int(rl["t_start"]), tz=timezone.utc).isoformat()
    results["run"] = {
        "file": C.DATA_FILE.name,
        "start_utc": start_utc,
        "span_min": rl["span_s"] / 60.0,
        "n_events": rl["n_events"],
        "rate_hz": rl["rate_hz"],
        "rate_per_hour": rl["rate_per_hour"],
        "rate_per_day": rl["rate_per_day"],
    }
    print(f"Rate: {rl['rate_hz']:.2f} Hz = {rl['rate_per_hour']:.0f} /hour "
          f"= {rl['rate_per_day']:.0f} /day (open-sky reference)")

    fmat = [features.event_features(e) for e in events]
    X, feat_names = features.feature_matrix(fmat)

    coinc = rates.fine_time_residuals(events)
    thetas = X[:, feat_names.index("theta_deg")]
    phis = X[:, feat_names.index("phi_deg")]
    valid = ~np.isnan(thetas)

    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    ax[0].hist(X[:, feat_names.index("total_hits")], bins=np.arange(1.5, 40.5), color="steelblue")
    ax[0].set_xlabel("Total hits per event")
    ax[0].set_ylabel("Events")
    ax[0].set_yscale("log")
    ax[1].hist(coinc, bins=60, color="seagreen")
    ax[1].set_xlabel("Plane-to-plane fine-time span (ns)")
    ax[1].set_ylabel("Events")
    ax[1].set_yscale("log")
    ax[1].axvline(200, color="crimson", ls="--", label="200 ns window")
    ax[1].legend()
    ax[2].hist(X[:, feat_names.index("max_cluster_size")], bins=np.arange(0.5, 12.5), color="indianred")
    ax[2].set_xlabel("Max cluster size")
    ax[2].set_ylabel("Events")
    fig.suptitle("PAUL open-sky calibration run 2024-04-12")
    fig.tight_layout()
    fig.savefig(C.FIG_DIR / "event_quality.png", dpi=160)
    plt.close(fig)

    fig = plt.figure(figsize=(14, 5))
    ax1 = fig.add_subplot(131, projection="hist2d" if False else None)
    h = ax1.hist2d(thetas[valid], np.cos(np.radians(thetas[valid])), bins=50)
    fig.colorbar(h[3], ax=ax1).set_label("Events")
    ax1.set_xlabel(r"$\theta$ (deg)")
    ax1.set_ylabel(r"$\cos\theta$")
    ax2 = fig.add_subplot(132, polar=True)
    sel = valid & (thetas < 80)
    ax2.hist(np.radians(phis[sel]), bins=36, color="darkorange")
    ax2.set_title("Azimuthal distribution")
    ax3 = fig.add_subplot(133)
    ax3.hist2d(phis[valid], thetas[valid], bins=48, cmap="viridis")
    ax3.set_xlabel(r"$\phi$ (deg)")
    ax3.set_ylabel(r"$\theta$ (deg)")
    fig.suptitle("Angular distributions (open sky)")
    fig.tight_layout()
    fig.savefig(C.FIG_DIR / "angular_open_sky.png", dpi=160)
    plt.close(fig)

    cos_fit_mask = valid & (thetas < 80)
    ct = np.cos(np.radians(thetas[cos_fit_mask]))
    ct_bins = np.linspace(0.55, 1.0, 16)
    obs_ct, edges = np.histogram(ct, bins=ct_bins)
    ctr = 0.5 * (edges[:-1] + edges[1:])
    ref_shape = ctr**2
    scale = float(np.sum(obs_ct * ref_shape) / np.sum(ref_shape**2))
    ref = ref_shape * scale
    chi2 = float(np.sum((obs_ct - ref) ** 2 / np.clip(np.sqrt(ref), 1, None) ** 2))
    results["angular"] = {
        "n_valid_tracks": int(valid.sum()),
        "note": "chi2 vs cos^2 shape scaled to data within acceptance (ct>0.55); "
                "absolute angles assume 300 mm plane spacing",
        "cos2_chi2": chi2,
        "n_cos_bins": int(len(obs_ct)),
        "theta_mean_deg": float(np.mean(thetas[valid])),
        "theta_median_deg": float(np.median(thetas[valid])),
        "theta_max_deg": float(np.percentile(thetas[valid], 99)),
    }

    occ = np.zeros((C.N_PLANES, C.N_STRIPS))
    csz_all = []
    for e in events:
        for hdr, chans, adcs in e["plane_rows"]:
            p = int(hdr[5])
            np.add.at(occ[p], chans, 1)
            csz_all.extend(
                c["size"] for c in cluster_strips(chans.astype(np.int64), adcs.astype(np.int64))
            )
    figo, axo = plt.subplots(1, 2, figsize=(13, 4))
    im = axo[0].imshow(occ, aspect="auto", cmap="inferno")
    figo.colorbar(im, ax=axo[0], label="hits in run")
    axo[0].set_xlabel("Strip channel")
    axo[0].set_ylabel("Plane")
    axo[0].set_yticks([0, 1, 2])
    axo[0].set_title("Strip occupancy (dead/hot strips show as dark/bright columns)")
    axo[1].hist(csz_all, bins=np.arange(0.5, 12.5), color="mediumpurple")
    axo[1].set_xlabel("Cluster size (adjacent strips)")
    axo[1].set_ylabel("Clusters")
    axo[1].set_yscale("log")
    axo[1].set_title("Cluster-size distribution")
    figo.tight_layout()
    figo.savefig(C.FIG_DIR / "occupancy_clusters.png", dpi=160)
    plt.close(figo)

    iso, scaler = ml_models.fit_isolation_forest(X[valid])
    scores = ml_models.anomaly_scores(iso, scaler, X[valid])
    thr = np.percentile(scores, 95)
    anomalous = scores > thr
    fig2, axf = plt.subplots(figsize=(7, 4.5))
    sc = axf.scatter(
        X[valid][:, feat_names.index("theta_deg")],
        np.log10(np.clip(X[valid][:, feat_names.index("total_adc")], 1, None)),
        c=scores, s=8, cmap="coolwarm",
    )
    fig2.colorbar(sc, label="anomaly score (higher = more anomalous)")
    axf.set_xlabel(r"$\theta$ (deg)")
    axf.set_ylabel(r"log$_{10}$ total ADC")
    axf.set_title("IsolationForest anomaly detection (open-sky run)")
    fig2.tight_layout()
    fig2.savefig(C.FIG_DIR / "anomaly_scores.png", dpi=160)
    plt.close(fig2)
    results["unsupervised"] = {
        "contamination": 0.05,
        "n_anomalous": int(anomalous.sum()),
        "score_threshold_p95": float(thr),
    }

    clean = features.clean_muon_mask(fmat)
    results["clean_fraction"] = {
        "n_clean": int(clean.sum()),
        "fraction": float(clean.mean()),
    }

    rng = np.random.default_rng(7)
    noise_events = features.synthesize_noise_events(rows, rng, n_out=len(events))
    noise_fmat = []
    for ev in noise_events:
        e = {
            "event": ev[0][0][1],
            "unix": ev[0][0][0],
            "fine": np.array([r[0][2] for r in ev]),
            "tdc": [(r[0][3], r[0][4]) for r in ev],
            "plane_rows": ev,
            "n_planes": len(ev),
            "coinc_span_ns": float((max(r[0][2] for r in ev) - min(r[0][2] for r in ev)) * C.FINE_UNIT_NS),
            "in_window": True,
        }
        noise_fmat.append(features.event_features(e))
    X_noise, _ = features.feature_matrix(noise_fmat)

    clf, metrics = ml_models.train_muon_noise_classifier(X[clean], X_noise)
    metrics["feature_names"] = [
        "n_planes", "coinc_span_ns", "total_hits", "mean_hits_per_plane",
        "total_adc", "max_adc", "n_clusters", "max_cluster_size",
        "adc_spread", "min_hits_plane", "theta_deg", "phi_deg", "y_res_mm",
    ]
    proba_real = clf.predict_proba(X)[:, 1]
    results["classifier"] = {
        "auc": metrics["auc"],
        "noise_flagged_fraction": float((proba_real < 0.5).mean()),
        "muon_flagged_fraction": float((proba_real >= 0.5).mean()),
        "n_train": metrics["n_train"],
        "n_test": metrics["n_test"],
    }

    importances = clf.feature_importances_
    order = np.argsort(importances)[::-1]
    fig3, axi = plt.subplots(figsize=(8, 5))
    axi.barh([metrics["feature_names"][i] for i in order][::-1],
             importances[order][::-1], color="slateblue")
    axi.set_xlabel("RandomForest importance")
    axi.set_title("Muon vs noise-proxy classifier feature importance")
    fig3.tight_layout()
    fig3.savefig(C.FIG_DIR / "rf_feature_importance.png", dpi=160)
    plt.close(fig3)

    surrogate, mse = ml_models.make_transmission_surrogate()
    depth_grid = np.logspace(np.log10(200), np.log10(8000), 120)
    T_grid = np.array([float(ml_models.surrogate_transmission(surrogate, x, 0.0)[0]) for x in depth_grid])

    r_uw_per_day = C.UNDERGROUND_RATE_PER_DAY
    ratio = r_uw_per_day / rl["rate_per_day"]
    x_exact, xs, ts = physics.depth_fit_from_ratio(ratio)
    x_ml = ml_models.solve_depth_from_ratio(surrogate, ratio)
    sigma_rel = 1.0 / np.sqrt(max(r_uw_per_day * C.UNDERGROUND_DAYS, 1))
    x_lo_band = physics.depth_fit_from_ratio(ratio * (1 + sigma_rel))[0]
    x_hi_band = physics.depth_fit_from_ratio(ratio * (1 - sigma_rel))[0]

    results["overburden"] = {
        "underground_rate_per_day_assumed": r_uw_per_day,
        "open_rate_per_day_measured": float(rl["rate_per_day"]),
        "transmission_ratio": float(ratio),
        "depth_mwe_exact_model": float(x_exact) if x_exact else None,
        "depth_mwe_ml_surrogate_integrated": float(x_ml) if x_ml else None,
        "depth_band_mwe_poisson": (
            [float(x_hi_band), float(x_lo_band)]
            if x_exact and x_lo_band and x_hi_band else None
        ),
        "meters_rock_at_2.65gcc": (
            float(physics.mwe_to_meters_rock(x_exact)) if x_exact else None
        ),
        "relative_rate_uncertainty": float(sigma_rel),
        "model_note": (
            "flat-overburden Gaisser spectrum + Groom range-energy in standard rock; "
            "5 events/day underground figure provided by collaboration"
        ),
    }

    fig4, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5))
    a1.plot(xs, ts, lw=2, label="analytic Gaisser+range model")
    a1.plot(depth_grid, np.clip(T_grid, 1e-16, None), "--", lw=2,
            label="ML surrogate (GradientBoosting)")
    a1.axhline(ratio, color="crimson", ls=":", label=f"measured ratio {ratio:.2e}")
    if x_exact:
        a1.axvline(x_exact, color="gray", ls="-.", alpha=0.7)
        a1.annotate(f"{x_exact:.0f} m.w.e.", (x_exact, ratio),
                    textcoords="offset points", xytext=(8, 10))
    a1.set_xscale("log")
    a1.set_yscale("log")
    a1.set_xlabel("Vertical overburden (m.w.e.)")
    a1.set_ylabel("Transmission $T$ (underground/surface rate)")
    a1.set_ylim(1e-9, 2)
    a1.legend(fontsize=8)
    a1.set_title("Muon transmission vs overburden")
    th_grid = np.linspace(0, 85, 90)
    TT = np.zeros((len(th_grid), len(xs)))
    for i, th in enumerate(th_grid):
        for j, xx in enumerate(xs):
            TT[i, j] = physics.directional_transmission(xx, th)
    im = a2.pcolormesh(xs, th_grid, np.clip(TT, 1e-12, None),
                       norm=matplotlib.colors.LogNorm(vmin=1e-12, vmax=1),
                       cmap="magma", shading="auto")
    fig4.colorbar(im, ax=a2, label="Transmission")
    a2.set_xscale("log")
    a2.set_xlabel("Vertical overburden (m.w.e.)")
    a2.set_ylabel(r"Zenith $\theta$ (deg)")
    a2.set_title("Directional transmission map (lab siting)")
    fig4.tight_layout()
    fig4.savefig(C.FIG_DIR / "transmission_overburden.png", dpi=160)
    plt.close(fig4)

    hourly_centers, hourly_counts = rates.hourly_series(events)
    fig5, axr = plt.subplots(figsize=(9, 4))
    width_h = max(rl["span_s"] / 3600.0 / 60.0, 0.02)
    minutes = (np.array([e["unix"] for e in events]) - rl["t_start"]) / 60.0
    axr.hist(minutes, bins=60, color="teal")
    axr.axvline(0); axr.axvline(rl["span_s"] / 60.0, ls="--", color="k")
    axr.set_xlabel("Minutes since run start")
    axr.set_ylabel("Events per minute-bin")
    axr.set_title(f"Open-sky stability — mean {rl['rate_hz']:.2f} Hz")
    fig5.tight_layout()
    fig5.savefig(C.FIG_DIR / "time_stability.png", dpi=160)
    plt.close(fig5)

    ml_models.save_model(clf, C.MODELS_DIR / "muon_vs_noise_rf.joblib")
    ml_models.save_model(iso, C.MODELS_DIR / "isolation_forest.joblib")
    ml_models.save_model(surrogate, C.MODELS_DIR / "transmission_surrogate.joblib")

    with open(C.RESULTS_DIR / "analysis_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
