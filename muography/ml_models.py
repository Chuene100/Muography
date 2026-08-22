import joblib
import numpy as np
from sklearn.ensemble import (
    GradientBoostingRegressor,
    IsolationForest,
    RandomForestClassifier,
)
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from .physics import gaisser_flux, min_energy_for_range


def fit_isolation_forest(X, contamination=0.05, seed=42):
    iso = IsolationForest(n_estimators=300, contamination=contamination,
                          random_state=seed, n_jobs=-1)
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    iso.fit(Xs)
    return iso, scaler


def anomaly_scores(iso, scaler, X):
    return -iso.score_samples(scaler.transform(X))


def train_muon_noise_classifier(X_muon, X_noise, seed=42):
    if len(X_muon) == 0 or len(X_noise) == 0:
        raise ValueError("Both muon and noise feature sets must be non-empty")
    X = np.vstack([X_muon, X_noise])
    y = np.concatenate([np.ones(len(X_muon)), np.zeros(len(X_noise))])
    if len(np.unique(y)) < 2:
        raise ValueError("Training data contains fewer than two classes")
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.3, random_state=seed, stratify=y
    )
    clf = RandomForestClassifier(
        n_estimators=400, max_depth=None, min_samples_leaf=2,
        class_weight="balanced", random_state=seed, n_jobs=-1,
    )
    clf.fit(X_tr, y_tr)
    proba = clf.predict_proba(X_te)[:, 1]
    pred = clf.predict(X_te)
    metrics = {
        "auc": float(roc_auc_score(y_te, proba)),
        "report": classification_report(y_te, pred, output_dict=True),
        "n_train": int(len(y_tr)),
        "n_test": int(len(y_te)),
        "feature_names": None,
    }
    return clf, metrics


def make_transmission_surrogate(x_max_mwe=8000.0, seed=42):
    rng = np.random.default_rng(seed)
    n = 20000
    depth = rng.uniform(0.0, x_max_mwe, n)
    theta_cos_sampled = np.degrees(np.arccos(rng.uniform(0.08, 1.0, n)))
    theta_near_vertical = np.abs(rng.normal(0.0, 12.0, n))
    pick = rng.random(n) < 0.35
    theta = np.where(pick, theta_near_vertical, theta_cos_sampled)
    theta = np.clip(theta, 0.0, 85.0)
    cos_t = np.cos(np.radians(theta))
    slant_gcm2 = depth * 100.0 / np.clip(cos_t, 1e-3, None)
    T = np.empty(n)
    for i in range(n):
        Emin = min_energy_for_range(slant_gcm2[i])
        logE = np.linspace(np.log10(0.5), np.log10(2e4), 2000)
        E = 10.0**logE
        dlogE = logE[1] - logE[0]
        w = gaisser_flux(E, cos_t[i])
        above = E > max(Emin, 0.5)
        total = float(np.sum(w * E) * dlogE * np.log(10))
        kept = float(np.sum(w[above] * E[above]) * dlogE * np.log(10))
        T[i] = kept / total if total > 0 else 0.0
    slant = depth * 100.0 / np.clip(cos_t, 1e-3, None)
    Xg = np.column_stack([
        np.log10(slant + 1.0),
        cos_t,
        np.log10(depth + 1.0),
    ])
    y = np.log10(np.clip(T, 1e-16, None))
    reg = GradientBoostingRegressor(n_estimators=600, learning_rate=0.05,
                                    max_depth=5, subsample=0.9,
                                    random_state=seed)
    reg.fit(Xg, y)
    return reg, float(np.mean((reg.predict(Xg) - y) ** 2))


def surrogate_transmission(reg, depth_mwe, theta_deg):
    depth = np.atleast_1d(np.asarray(depth_mwe, dtype=float))
    th = np.atleast_1d(np.radians(np.asarray(theta_deg, dtype=float)))
    c = np.clip(np.cos(th), 1e-3, None)
    slant = depth * 100.0 / c
    X = np.column_stack([
        np.log10(slant + 1.0),
        c,
        np.log10(depth + 1.0),
    ])
    return 10.0 ** reg.predict(X)


def integrated_surrogate_transmission(reg, depth_mwe, theta_max_deg=85.0, n_theta=60):
    ths = np.radians(np.linspace(0.5, theta_max_deg, n_theta))
    vals = np.array([
        float(surrogate_transmission(reg, depth_mwe, np.degrees(t))[0]) for t in ths
    ])
    w = np.sin(ths)
    return float(np.sum(vals * w) / np.sum(w))


def solve_depth_from_ratio(reg, ratio, x_lo=100.0, x_hi=9000.0):
    lo, hi = x_lo, x_hi
    f = lambda x: np.log10(integrated_surrogate_transmission(reg, x)) - np.log10(ratio)
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return None
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def save_model(obj, path):
    joblib.dump(obj, str(path))


def load_model(path):
    return joblib.load(str(path))
