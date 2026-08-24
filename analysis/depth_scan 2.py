from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from muography.dataio import parse_paul_dat
from muography.events import group_events
from muography.tracking import reconstruct_track

OUTPUT_DIR = PROJECT_ROOT / "muon-sim" / "output"
FIG_DIR = PROJECT_ROOT / "analysis" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Each of these simulations used /run/beamOn 50000.
N_PRIMARIES = 50_000
depths_m = np.array([0, 100, 250, 500, 750, 1000])

n_detected = []
theta_by_depth = {}

for depth in depths_m:
    data_file = OUTPUT_DIR / f"depth_{depth}m.dat"
    rows = parse_paul_dat(data_file)
    events = group_events(rows)

    n_detected.append(len(events))

    theta = []
    for event in events:
        track = reconstruct_track(event)
        if track is not None:
            theta.append(track["theta_deg"])
    theta_by_depth[depth] = np.asarray(theta)

n_detected = np.asarray(n_detected)
acceptance = n_detected / N_PRIMARIES
transmission = acceptance / acceptance[0]

# Experiment 1: attenuation/transmission vs rock depth
fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogy(depths_m, transmission, "o-", lw=2, color="firebrick")
ax.set_xlabel("Rock thickness (m)")
ax.set_ylabel("Relative transmission")
ax.set_title("Simulated muon transmission through rock")
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(FIG_DIR / "simulated_depth_transmission.png", dpi=160)
plt.show()

# Experiment 2: angular distributions at different depths
fig, ax = plt.subplots(figsize=(8, 5))
for depth in depths_m:
    theta = theta_by_depth[depth]
    if len(theta):
        ax.hist(
            theta,
            bins=np.linspace(0, 90, 37),
            histtype="step",
            linewidth=2,
            density=True,
            label=f"{depth} m",
        )

ax.set_xlabel(r"Zenith angle $\theta$ (degrees)")
ax.set_ylabel("Normalised event density")
ax.set_title("Muon angular distribution after rock overburden")
ax.legend(title="Rock thickness")
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(FIG_DIR / "simulated_angular_by_depth.png", dpi=160)
plt.show()

# Table of results
for depth, count, acc, trans in zip(depths_m, n_detected, acceptance, transmission):
    print(
        f"{depth:4d} m : {count:6d} detected | "
        f"acceptance = {acc:.5f} | transmission = {trans:.5f}"
    )