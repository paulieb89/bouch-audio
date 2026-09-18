#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""BS.1770-4 integrated loudness, true peak, clipping, stereo and spectral
report for a rendered WAV, as JSON on stdout.

Provenance: Audio Agent Workbench V2 `tools/analyze.py` at bc460db, itself a
port of REAPER Agent Lab V1's `analyze.py` (cross-checked there against
ffmpeg's `ebur128`/`astats` to 0.08 LU). See evidence/PROVENANCE.md.

Usage:
    analyze.py render.wav [--sections sections.json]
    analyze.py render.wav --window START_S DURATION_S

sections.json (optional): [["name", start_s, end_s], ...] for a per-section
breakdown (mean short-term loudness, peak) in addition to the whole-file
report.

--window START_S DURATION_S runs the same report function on a bounded
slice instead of the whole file. It exists because a whole-file aggregate
could not see an FM attack transient that a 21 ms window could (V2
designed-sound-palette-01). Not a second analyser: the slice is handed to
the same `compute_report()` the whole-file path uses. Fields that need more
samples than a short window has (`lufs_integrated` needs >=400ms, `lra_lu`
needs >=2 short-term blocks) come back `null` rather than a misleading
number. Mutually exclusive with `--sections`.

Proves technical properties only. It cannot say whether audio sounds good.
"""
import json
import sys
import wave

import numpy as np
from scipy.signal import lfilter, resample_poly, welch

# numpy 2 deprecates trapz in favour of trapezoid; numpy 1.x lacks trapezoid.
_trapezoid = getattr(np, "trapezoid", None) or np.trapz


def read_wav(path):
    w = wave.open(path, "rb")
    ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
    raw = w.readframes(n)
    w.close()
    if sw == 2:
        a = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    elif sw == 3:
        b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3).astype(np.int32)
        v = b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)
        v = np.where(v & 0x800000, v - (1 << 24), v)
        a = v.astype(np.float64) / 8388608.0
    elif sw == 4:
        a = np.frombuffer(raw, dtype="<i4").astype(np.float64) / 2147483648.0
    else:
        raise ValueError(f"sampwidth {sw}")
    return a.reshape(-1, ch), sr


def biquad_shelf(fs, f0=1681.974450955533, G=3.999843853973347, Q=0.7071752369554196):
    """BS.1770 pre-filter (high shelf), designed for any fs by bilinear
    transform with the parameters libebur128/ffmpeg use. At 48 kHz this
    reproduces the coefficients tabulated in ITU-R BS.1770.

    Corrected on promotion to bouch-audio: the V1/V2 version fed these same
    parameters into the RBJ cookbook shelf formula, which they were not
    derived for, and read about 0.25 LU low on 1 kHz-centred material
    (see evidence/qualification.md)."""
    K = np.tan(np.pi * f0 / fs)
    Vh = 10 ** (G / 20)
    Vb = Vh ** 0.4996667741545416
    a0 = 1 + K / Q + K * K
    b = np.array([Vh + Vb * K / Q + K * K, 2 * (K * K - Vh), Vh - Vb * K / Q + K * K]) / a0
    a = np.array([1.0, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0])
    return b, a


def biquad_hp(fs, f0=38.13547087602444, Q=0.5003270373238773):
    """BS.1770 RLB high-pass, same bilinear design as biquad_shelf."""
    K = np.tan(np.pi * f0 / fs)
    a0 = 1 + K / Q + K * K
    b = np.array([1.0, -2.0, 1.0])
    a = np.array([1.0, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0])
    return b, a


def k_weight(x, fs):
    b1, a1 = biquad_shelf(fs)
    b2, a2 = biquad_hp(fs)
    return lfilter(b2, a2, lfilter(b1, a1, x, axis=0), axis=0)


def loudness(x, fs, block=0.400, overlap=0.75):
    y = k_weight(x, fs)
    hop = int(fs * block * (1 - overlap))
    bl = int(fs * block)
    if len(y) < bl:
        return None, None, np.array([]), None
    nb = 1 + (len(y) - bl) // hop
    idx = np.arange(bl)[None, :] + hop * np.arange(nb)[:, None]
    ms = (y[idx] ** 2).mean(axis=1)
    z = ms.sum(axis=1)
    with np.errstate(divide="ignore"):
        lk = -0.691 + 10 * np.log10(np.maximum(z, 1e-20))
    keep = lk > -70.0
    if not keep.any():
        return None, None, lk, None
    rel = -0.691 + 10 * np.log10(z[keep].mean()) - 10.0
    keep2 = keep & (lk > rel)
    integ = -0.691 + 10 * np.log10(z[keep2].mean()) if keep2.any() else None
    return integ, rel, lk, keep2


def short_term(x, fs):
    _, _, lk, _ = loudness(x, fs, block=3.0, overlap=2.0 / 3.0)
    return lk


def lra(x, fs):
    st = short_term(x, fs)
    st = st[st > -70]
    if len(st) < 2:
        return None
    abs_gated = st[st > (10 * np.log10(np.mean(10 ** (st / 10))) - 20)]
    if len(abs_gated) < 2:
        return None
    return float(np.percentile(abs_gated, 95) - np.percentile(abs_gated, 10))


def true_peak_db(x, fs):
    up = resample_poly(x, 4, 1, axis=0)
    p = np.max(np.abs(up))
    return float(20 * np.log10(p)) if p > 0 else float("-inf")


def band_energy(x, fs):
    mono = x.mean(axis=1)
    f, P = welch(mono, fs, nperseg=8192)
    tot = _trapezoid(P, f)
    bands = [
        ("sub_20_60", 20, 60), ("bass_60_150", 60, 150), ("lowmid_150_400", 150, 400),
        ("mid_400_2k", 400, 2000), ("hi_2k_6k", 2000, 6000), ("air_6k_20k", 6000, 20000),
    ]
    out = {}
    for nm, lo, hi in bands:
        m = (f >= lo) & (f < hi)
        e = _trapezoid(P[m], f[m]) if m.any() else 0.0
        out[nm] = float(100 * e / tot) if tot > 0 else 0.0
    centroid = float(_trapezoid(P * f, f) / tot) if tot > 0 else 0.0
    return out, centroid


def silence_runs(x, fs, thresh_db=-60, min_run_s=0.5):
    env = np.abs(x).max(axis=1)
    win = max(1, int(fs * 0.05))
    usable = len(env) // win * win
    if usable == 0:
        return []
    e = env[:usable].reshape(-1, win).max(axis=1)
    sil = e < 10 ** (thresh_db / 20)
    runs, cur = [], 0
    for s in sil:
        if s:
            cur += 1
        elif cur:
            runs.append(cur * 0.05)
            cur = 0
    if cur:
        runs.append(cur * 0.05)
    return [round(r, 2) for r in runs if r >= min_run_s]


def compute_report(x, fs, path):
    """The metric suite, applied to whatever slice of samples it's given.
    Whole-file mode and --window mode both call this on their own slice of
    `x` — the metrics themselves have no idea which one they're in."""
    dur = len(x) / fs
    integ, _, _, _ = loudness(x, fs)
    st = short_term(x, fs)
    gated_st = st[st > -70] if st.size else st
    tp = true_peak_db(x, fs)
    sp = float(np.max(np.abs(x))) if x.size else 0.0
    clip = int(np.sum(np.abs(x) >= 0.9999))
    if x.shape[1] >= 2:
        L, R = x[:, 0], x[:, 1]
        corr = float(np.corrcoef(L, R)[0, 1])
        side, mid = (L - R) / 2, (L + R) / 2
        ms_ratio = float(20 * np.log10(np.sqrt((side ** 2).mean()) / max(np.sqrt((mid ** 2).mean()), 1e-12)))
    else:
        corr, ms_ratio = None, None
    bands, centroid = band_energy(x, fs)

    return {
        "file": path,
        "duration_s": round(dur, 3),
        "sample_rate": fs,
        "channels": x.shape[1],
        "lufs_integrated": round(integ, 2) if integ is not None else None,
        "lufs_short_term_max": round(float(np.max(gated_st)), 2) if gated_st.size else None,
        "lra_lu": round(v, 2) if (v := lra(x, fs)) is not None else None,
        "sample_peak_dbfs": round(20 * np.log10(sp), 2) if sp > 0 else float("-inf"),
        "true_peak_dbtp": round(tp, 2),
        "clipped_samples": clip,
        "stereo_correlation": round(corr, 3) if corr is not None else None,
        "side_mid_ratio_db": round(ms_ratio, 2) if ms_ratio is not None else None,
        "spectral_centroid_hz": round(centroid, 1),
        "band_energy_pct": {k: round(v, 1) for k, v in bands.items()},
        "silence_runs_ge_0.5s": silence_runs(x, fs),
    }


def analyze(path, sections=None, window=None):
    x, fs = read_wav(path)
    file_dur = len(x) / fs

    if window is not None:
        start, dur_w = window
        if dur_w <= 0:
            raise ValueError(f"window duration must be > 0, got {dur_w}")
        if start < 0 or start + dur_w > file_dur + 1e-9:
            raise ValueError(
                f"window [{start}, {round(start + dur_w, 6)}]s is out of bounds "
                f"for a {round(file_dur, 3)}s file"
            )
        start_i, end_i = int(round(start * fs)), int(round((start + dur_w) * fs))
        report = compute_report(x[start_i:end_i], fs, path)
        report["window_s"] = [round(start, 6), round(start + dur_w, 6)]
        return report

    report = compute_report(x, fs, path)

    if sections:
        section_reports = []
        for nm, a, b in sections:
            seg = x[int(a * fs):int(b * fs)]
            if len(seg) < fs:
                continue
            i2, _, _, _ = loudness(seg, fs)
            pk = 20 * np.log10(max(np.max(np.abs(seg)), 1e-9))
            section_reports.append({"name": nm, "start_s": a, "lufs_short_term_mean": round(i2, 2) if i2 is not None else None, "peak_dbfs": round(pk, 2)})
        report["sections"] = section_reports

    return report


def main():
    usage = "usage: analyze.py render.wav [--sections sections.json | --window START_S DURATION_S]"
    if len(sys.argv) < 2:
        print(usage, file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    if "--sections" in sys.argv and "--window" in sys.argv:
        print("--sections and --window are mutually exclusive", file=sys.stderr)
        sys.exit(2)
    sections = None
    window = None
    if "--sections" in sys.argv:
        sections_path = sys.argv[sys.argv.index("--sections") + 1]
        with open(sections_path) as f:
            sections = json.load(f)
    if "--window" in sys.argv:
        i = sys.argv.index("--window")
        try:
            window = (float(sys.argv[i + 1]), float(sys.argv[i + 2]))
        except (IndexError, ValueError):
            print("usage: analyze.py render.wav --window START_S DURATION_S", file=sys.stderr)
            sys.exit(2)
    try:
        report = analyze(path, sections, window)
    except ValueError as e:
        print(f"analyze.py: {e}", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
