import numpy as np


def parse_paul_dat(path):
    rows = []
    with open(path) as f:
        for line in f:
            tok = line.split()
            if len(tok) < 10:
                continue
            hdr = np.array([int(t) for t in tok[:9]], dtype=np.int64)
            rest = np.array([int(t) for t in tok[9:]], dtype=np.int64)
            nhits = int(hdr[8])
            n_pairs = min(nhits, len(rest) // 2)
            chans = rest[: 2 * n_pairs : 2]
            adcs = rest[1 : 2 * n_pairs : 2]
            rows.append((hdr, chans, adcs))
    return rows


def data_quality(rows):
    n_rows = len(rows)
    bad_nhits = 0
    out_of_range = 0
    adc_clipped = 0
    for hdr, chans, adcs in rows:
        if int(hdr[8]) != len(chans):
            bad_nhits += 1
        if np.any(chans > 63) or np.any(adcs > 4095):
            out_of_range += 1
        if np.any(adcs >= 4095):
            adc_clipped += 1
    return {
        "n_plane_rows": n_rows,
        "rows_with_nhits_mismatch": bad_nhits,
        "rows_with_out_of_range_values": out_of_range,
        "rows_with_saturated_adc": adc_clipped,
    }
