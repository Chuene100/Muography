import numpy as np

ALPHA = 2.44e-3
BETA = 4.06e-6
RHO_ROCK = 2.65


def gaisser_flux(E_GeV, cos_theta):
    E = np.asarray(E_GeV, dtype=float)
    c = np.clip(np.asarray(cos_theta, dtype=float), 1e-6, 1.0)
    return (
        0.14
        * E ** (-2.7)
        * (
            1.0 / (1.0 + 1.1 * E * c / 115.0)
            + 0.054 / (1.0 + 1.1 * E * c / 850.0)
        )
    )


def muon_range_gcm2(E_GeV):
    E = np.asarray(E_GeV, dtype=float)
    return np.log1p(BETA * E / ALPHA) / BETA


def min_energy_for_range(range_gcm2):
    X = np.asarray(range_gcm2, dtype=float)
    return (np.expm1(BETA * X) * ALPHA) / BETA


def transmission_exact(depth_mwe, theta_max_deg=85.0, n_theta=60, e_min=0.5, n_e=400):
    X_vertical_gcm2 = depth_mwe * 100.0
    thetas = np.radians(np.linspace(0.5, theta_max_deg, n_theta))
    logE = np.linspace(np.log10(e_min), np.log10(2e4), n_e)
    E = 10.0**logE
    dlogE = logE[1] - logE[0]
    num = 0.0
    den = 0.0
    for th in thetas:
        slant = X_vertical_gcm2 / max(np.cos(th), 1e-3)
        Emin_th = min_energy_for_range(slant)
        w = gaisser_flux(E, np.cos(th)) * np.sin(th)
        mask = E > max(Emin_th, e_min)
        num += float(np.sum(w[mask] * E[mask]) * dlogE * np.log(10))
        den += float(np.sum(w * E) * dlogE * np.log(10))
    return num / den if den > 0 else 0.0


def depth_fit_from_ratio(ratio, x_lo=200.0, x_hi=8000.0):
    xs = np.logspace(np.log10(x_lo), np.log10(x_hi), 40)
    ts = []
    for x in xs:
        ts.append(transmission_exact(x))
    ts = np.array(ts)
    logt = np.log10(ts)
    target = np.log10(ratio)
    if target > logt.max() or target < logt.min():
        return None, xs, ts
    idx = np.argsort(np.abs(logt - target))[:2]
    i0, i1 = sorted(idx)
    frac = (target - logt[i0]) / (logt[i1] - logt[i0])
    x_fit = 10 ** (np.log10(xs[i0]) + frac * (np.log10(xs[i1]) - np.log10(xs[i0])))
    return x_fit, xs, ts


def directional_transmission(depth_mwe, theta_deg, e_min=0.5, n_e=400):
    c = max(np.cos(np.radians(theta_deg)), 1e-3)
    slant = depth_mwe * 100.0 / c
    Emin = min_energy_for_range(slant)
    logE = np.linspace(np.log10(e_min), np.log10(2e4), n_e)
    E = 10.0**logE
    w = gaisser_flux(E, c)
    mask = E > max(Emin, e_min)
    den = float(np.sum(w * E))
    num = float(np.sum(w[mask] * E[mask]))
    return num / den if den > 0 else 0.0


def mwe_to_meters_rock(x_mwe, rho=RHO_ROCK):
    return x_mwe / rho
