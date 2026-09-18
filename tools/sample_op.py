#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Offline sample operations with self-verifying manifests.

    ./sample_op.py slice   SRC --cuts 0.5s,0.75s,1s   --out-dir D --prefix NAME
    ./sample_op.py slice   SRC --ranges 0.5s-0.6s,2s-2.1s --out-dir D --prefix NAME
    ./sample_op.py reverse SRC --out OUT.wav
    ./sample_op.py repitch SRC --semitones -5 --out OUT.wav
    ./sample_op.py arrange --out OUT.wav a.wav gap:250ms b.wav ...   (or @items.txt)
    ./sample_op.py verify  MANIFEST.json

Times are "<n>s", "<n>ms" or a bare integer sample count. Every operation
writes 24-bit (or wider) PCM, reads its own output back, runs its checks and
writes <out>.manifest.json. Exit 0 = every required check passed.

Checks prove technical postconditions only (finite, not clipped, valid WAV,
exact nulls, lengths, click-free edit boundaries). They say nothing about
whether the result sounds good.

Requires numpy and scipy. analyze.py (read_wav) must sit beside this file.
"""
import argparse, hashlib, json, math, os, sys, wave
from fractions import Fraction
import numpy as np
from scipy.signal import resample_poly

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
from analyze import read_wav

VERSION = 1
DEFAULT_FADE_MS = 3.0        # raised-cosine edge fade; short enough not to soften attacks audibly
QUIET_EDGE = 1e-3            # -60 dBFS: an edge this quiet needs no fade under policy "auto"
EDGE_SAMPLES = 4             # samples inspected at each edge (catches slope, not just value)
CLICK_WIN_MS = 10.0          # neighbourhood used as the "normal" second-difference level
CLICK_RATIO = 8.0            # boundary |d2| above ratio x neighbourhood median ...
CLICK_FLOOR = 1e-3           # ... and above this absolute level counts as a click
MAX_DENOMINATOR = 1000       # resample ratio limit; <= 0.03 cents from equal temperament over +-24 st


# ------------------------------------------------------------------ io
def rel(path):
    """Manifest paths are relative to the working directory the tool runs in
    (the V1 original used its own repository root, which is meaningless once
    the tool is installed inside a plugin). Run `verify` from that directory."""
    base = os.getcwd()
    p = os.path.abspath(path)
    return os.path.relpath(p, base) if p.startswith(base + os.sep) else p

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def load(path):
    with wave.open(path, "rb") as w:
        bits = 8 * w.getsampwidth()
    x, sr = read_wav(path)
    return x, sr, bits

def describe(path):
    with wave.open(path, "rb") as w:
        return dict(path=rel(path), sha256=sha256(path), frames=w.getnframes(),
                    sample_rate=w.getframerate(), channels=w.getnchannels(), bits=8 * w.getsampwidth())

def quantize(x, bits):
    s = 2 ** (bits - 1)
    return np.clip(np.round(x * s), -s, s - 1).astype(np.int64)

def write_wav(path, x, sr, bits):
    q = quantize(x, bits)
    if bits == 16:
        raw = q.astype("<i2").tobytes()
    elif bits == 24:
        v = q.reshape(-1).astype(np.int32)
        b = np.empty((v.size, 3), dtype=np.uint8)
        b[:, 0] = v & 0xFF; b[:, 1] = (v >> 8) & 0xFF; b[:, 2] = (v >> 16) & 0xFF
        raw = b.tobytes()
    elif bits == 32:
        raw = q.astype("<i4").tobytes()
    else:
        raise ValueError(f"bits {bits}")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(x.shape[1]); w.setsampwidth(bits // 8); w.setframerate(sr)
        w.writeframes(raw)

def parse_time(s, sr):
    s = s.strip()
    if s.endswith("ms"):
        v = round(float(s[:-2]) * sr / 1000.0)
    elif s.endswith("s"):
        v = round(float(s[:-1]) * sr)
    else:
        v = int(s)
    if v < 0:
        raise ValueError(f"negative time {s}")
    return int(v)


# ------------------------------------------------------------------ primitives
def fade_curve(n):
    """Raised-cosine 0 -> ~1 over n samples; first sample exactly 0."""
    return np.sin(0.5 * np.pi * np.arange(n) / n) ** 2 if n else np.ones(0)

def apply_fades(y, n_fade, policy):
    """Fade an edge only where needed. Returns (y, fade_in_samples, fade_out_samples)."""
    y = y.copy()
    n_fade = min(n_fade, len(y) // 2)
    def loud(edge):
        return edge.size and np.max(np.abs(edge)) > QUIET_EDGE
    fin = n_fade if policy == "always" or (policy == "auto" and loud(y[:EDGE_SAMPLES])) else 0
    fout = n_fade if policy == "always" or (policy == "auto" and loud(y[-EDGE_SAMPLES:])) else 0
    if fin:
        y[:fin] *= fade_curve(fin)[:, None]
    if fout:
        y[-fout:] *= fade_curve(fout)[::-1][:, None]
    return y, fin, fout

def ratio_for(semitones, max_denominator=MAX_DENOMINATOR):
    """Same rational resample_poly approach as undertow/compose.py pitch_shift
    (which used max_denominator=160)."""
    return Fraction(2 ** (-semitones / 12.0)).limit_denominator(max_denominator)

def pitch_shift(x, semitones, max_denominator=MAX_DENOMINATOR):
    """Varispeed: pitch and duration change together."""
    fr = ratio_for(semitones, max_denominator)
    if fr == 1:
        return x.copy(), fr
    return resample_poly(x, fr.numerator, fr.denominator, axis=0), fr


# ------------------------------------------------------------------ checks
def check(name, passed, required=True, **measured):
    return dict(name=name, passed=bool(passed), required=required, **measured)

def signal_checks(y, bits, allow_clip):
    """Pre-write: finite and within the representable range."""
    finite = bool(np.isfinite(y).all())
    out = [check("finite", finite, nonfinite_samples=int(np.size(y) - np.isfinite(y).sum()))]
    if finite:
        s = 2 ** (bits - 1)
        r = np.round(y * s)
        n = int(np.sum((r > s - 1) | (r < -s)))
        out.append(check("no_clipping", n == 0 or allow_clip, clipped_samples=n, allow_clip=allow_clip,
                         peak_dbfs=round(20 * math.log10(max(float(np.max(np.abs(y))), 1e-12)), 3)))
    return out

def readback_checks(path, y, sr, bits):
    """Post-write: the file is a valid WAV with the intended format and exact content."""
    try:
        d = describe(path)
        z, _, _ = load(path)
    except Exception as e:                                   # noqa: BLE001 -- any failure is a failed check
        return [check("valid_wav", False, error=repr(e))], None
    fmt_ok = (d["sample_rate"], d["channels"], d["bits"], d["frames"]) == (sr, y.shape[1], bits, len(y))
    exact = fmt_ok and np.array_equal(z, quantize(y, bits) / 2 ** (bits - 1))
    return [check("valid_wav", True),
            check("format_matches", fmt_ok, expected=dict(sample_rate=sr, channels=int(y.shape[1]), bits=bits, frames=len(y)),
                  actual={k: d[k] for k in ("sample_rate", "channels", "bits", "frames")}),
            check("content_matches_intended", exact)], z

def null_check(name, got, expected, required=True):
    """Exact null. Both arrays are float reads of integer PCM, so equal means bit-identical."""
    if got.shape != expected.shape:
        return check(name, False, required, reason="shape", got=list(got.shape), expected=list(expected.shape))
    diff = float(np.max(np.abs(got - expected))) if got.size else 0.0
    return check(name, diff == 0.0, required, samples=int(len(got)), max_abs_diff=diff,
                 residual_dbfs=None if diff == 0 else round(20 * math.log10(diff), 2))

def boundary_scores(y, sr, positions):
    """Discontinuity at each boundary, treating the signal as silent outside [0, len].
    Score = peak |second difference| touching the boundary / median |second difference|
    over the busier of the two neighbouring windows."""
    win = max(8, int(sr * CLICK_WIN_MS / 1000))
    pad = np.zeros((win + 3, y.shape[1]))
    z = np.vstack([pad, y, pad]); o = win + 3
    d2 = np.max(np.abs(np.diff(z, n=2, axis=0)), axis=1)    # d2[i] spans z[i..i+2]
    out = []
    for p in positions:
        b = p + o                                            # boundary sits between z[b-1] and z[b]
        peak = float(np.max(d2[b - 3: b + 1]))
        ref = max(float(np.median(d2[b - 3 - win: b - 3])), float(np.median(d2[b + 1: b + 1 + win])))
        score = peak / max(ref, 1e-9)
        out.append(dict(position=int(p), time_s=round(p / sr, 6), peak_d2=round(peak, 6), ratio=round(score, 2),
                        click=bool(peak > CLICK_FLOOR and score > CLICK_RATIO)))
    return out

def boundary_check(y, sr, positions, required=True):
    sc = boundary_scores(y, sr, sorted(set(positions)))
    bad = [s for s in sc if s["click"]]
    return check("boundaries_click_free", not bad, required, boundaries=len(sc), clicks=bad,
                 worst_ratio=max((s["ratio"] for s in sc), default=0.0), ratio_threshold=CLICK_RATIO, floor=CLICK_FLOOR)

def repitch_length_check(src_frames, out_frames, semitones, fr, max_cents):
    expect = math.ceil(src_frames * fr.numerator / fr.denominator) if fr != 1 else src_frames
    ideal = src_frames * 2 ** (-semitones / 12.0)
    cents = 1200 * math.log2(float(fr) / 2 ** (-semitones / 12.0))
    return [check("length_matches_ratio", out_frames == expect, expected_frames=expect, actual_frames=out_frames,
                  ratio=f"{fr.numerator}/{fr.denominator}"),
            check("ratio_within_cents", abs(cents) <= max_cents, cents_error=round(cents, 4), max_cents=max_cents,
                  ideal_frames=round(ideal, 2), deviation_from_ideal_frames=round(out_frames - ideal, 2))]


# ------------------------------------------------------------------ output + manifest
def emit(path, y, sr, bits, allow_clip, extra_checks=lambda z: []):
    """Write one output and run general + op-specific checks on what was actually written."""
    checks = signal_checks(y, bits, allow_clip)
    if not all(c["passed"] for c in checks if c["name"] == "finite"):
        return dict(path=rel(path), written=False), checks
    write_wav(path, y, sr, bits)
    rb, z = readback_checks(path, y, sr, bits)
    checks += rb
    if z is not None:
        checks += extra_checks(z)
    return dict(describe(path), written=True), checks

def finish(manifest_path, operation, params, sources, outputs, checks, notes=None):
    passed = all(c["passed"] for c in checks if c["required"])
    m = dict(tool="sample_op", version=VERSION, operation=operation, params=params, sources=sources,
             outputs=outputs, checks=checks, passed=passed)
    if notes:
        m["notes"] = notes
    with open(manifest_path, "w") as f:
        json.dump(m, f, indent=1)
    failed = [c["name"] + (f"[{c['output']}]" if "output" in c else "") for c in checks if c["required"] and not c["passed"]]
    print(json.dumps(dict(passed=passed, manifest=rel(manifest_path), outputs=[o["path"] for o in outputs], failed=failed)))
    return 0 if passed else 1

def tag(checks, i):
    for c in checks:
        c["output"] = i
    return checks

def manifest_for(out):
    return os.path.splitext(out)[0] + ".manifest.json"


# ------------------------------------------------------------------ operations
def op_slice(a):
    x, sr, sbits = load(a.src)
    bits = max(24, sbits); n_fade = round(a.fade_ms * sr / 1000)
    if bool(a.cuts) == bool(a.ranges):
        raise SystemExit("give exactly one of --cuts or --ranges")
    if a.cuts:
        c = [parse_time(t, sr) for t in a.cuts.split(",")]
        if c != sorted(c) or len(set(c)) != len(c) or len(c) < 2:
            raise SystemExit("--cuts must be at least two strictly increasing points")
        bounds = list(zip(c[:-1], c[1:]))
    else:
        bounds = [tuple(parse_time(t, sr) for t in r.split("-")) for r in a.ranges.split(",")]
    for s, e in bounds:
        if not 0 <= s < e <= len(x):
            raise SystemExit(f"slice {s}-{e} outside source (0-{len(x)} samples)")
    outputs, checks, readbacks = [], [], []
    for i, (s, e) in enumerate(bounds):
        y, fin, fout = apply_fades(x[s:e], n_fade, a.fade)
        path = os.path.join(a.out_dir, f"{a.prefix}_{i:02d}.wav")
        def extra(z, s=s, e=e, fin=fin, fout=fout):
            n = e - s
            return [null_check("unfaded_region_exact", z[fin:n - fout], x[s + fin:e - fout]),
                    boundary_check(z, sr, [0, n], required=a.fade != "none")]
        o, ch = emit(path, y, sr, bits, a.allow_clip, extra)
        outputs.append(dict(o, index=i, source_range=[s, e], fade_in_samples=fin, fade_out_samples=fout))
        checks += tag(ch, i)
        readbacks.append((fin, fout, load(path)[0] if o["written"] else None))
    if a.cuts:
        if all(fin == fout == 0 for fin, fout, _ in readbacks) and all(r is not None for *_, r in readbacks):
            checks.append(null_check("reconstruction_null", np.vstack([r for *_, r in readbacks]), x[bounds[0][0]:bounds[-1][1]]))
        else:
            checks.append(check("reconstruction_null", True, required=False, skipped="fades applied; run with --fade none for the control path"))
    params = dict(bounds=[list(b) for b in bounds], mode="cuts" if a.cuts else "ranges", fade_ms=a.fade_ms, fade=a.fade,
                  allow_clip=a.allow_clip)
    return finish(os.path.join(a.out_dir, f"{a.prefix}.manifest.json"), "slice", params, [describe(a.src)], outputs, checks)

def op_reverse(a):
    x, sr, sbits = load(a.src)
    bits = max(24, sbits)
    y, fin, fout = apply_fades(x[::-1], round(a.fade_ms * sr / 1000), a.fade)
    n = len(x)
    def extra(z):
        expected = x[n - 1::-1]                              # x[n-1-i] for i in 0..n-1
        return [null_check("reverse_null_unfaded_region", z[fin:n - fout], expected[fin:n - fout]),
                boundary_check(z, sr, [0, n], required=a.fade != "none")]
    o, checks = emit(a.out, y, sr, bits, a.allow_clip, extra)
    params = dict(fade_ms=a.fade_ms, fade=a.fade, allow_clip=a.allow_clip)
    return finish(manifest_for(a.out), "reverse", params, [describe(a.src)],
                  [dict(o, fade_in_samples=fin, fade_out_samples=fout)], checks)

def op_repitch(a):
    x, sr, sbits = load(a.src)
    bits = max(24, sbits)
    raw, fr = pitch_shift(x, a.semitones, a.max_denominator)
    y, fin, fout = apply_fades(raw, round(a.fade_ms * sr / 1000), a.fade)
    def extra(z):
        return repitch_length_check(len(x), len(z), a.semitones, fr, a.max_cents) + \
               [boundary_check(z, sr, [0, len(z)], required=a.fade != "none")]
    o, checks = emit(a.out, y, sr, bits, a.allow_clip, extra)
    dur = dict(source_s=round(len(x) / sr, 6), output_s=round(len(y) / sr, 6), duration_ratio=round(len(y) / len(x), 6),
               note="varispeed: duration changes with pitch")
    params = dict(semitones=a.semitones, ratio=f"{fr.numerator}/{fr.denominator}", max_denominator=a.max_denominator,
                  max_cents=a.max_cents, fade_ms=a.fade_ms, fade=a.fade, allow_clip=a.allow_clip)
    return finish(manifest_for(a.out), "repitch", params, [describe(a.src)],
                  [dict(o, duration=dur, fade_in_samples=fin, fade_out_samples=fout)], checks)

def op_arrange(a):
    loaded, sources, sr, ch, bits = [], {}, None, None, 24
    for it in a.items:
        if it.startswith("gap:"):
            loaded.append(("gap", it[4:]))
            continue
        x, isr, ibits = load(it)
        if sr is None:
            sr, ch = isr, x.shape[1]
        if (isr, x.shape[1]) != (sr, ch):
            raise SystemExit(f"{it}: {isr} Hz/{x.shape[1]} ch differs from first item {sr} Hz/{ch} ch")
        bits = max(bits, ibits)
        sources.setdefault(os.path.abspath(it), describe(it))
        loaded.append(("audio", it, x))
    if sr is None:
        raise SystemExit("arrange needs at least one audio item")
    n_fade = round(a.fade_ms * sr / 1000)
    parts, layout, pos = [], [], 0
    for item in loaded:
        if item[0] == "gap":
            g = parse_time(item[1], sr)
            parts.append(np.zeros((g, ch))); layout.append(dict(gap_samples=g, offset=pos)); pos += g
            continue
        _, path, x = item
        y, fin, fout = apply_fades(x, n_fade, a.fade)
        parts.append(y)
        layout.append(dict(item=rel(path), sha256=sources[os.path.abspath(path)]["sha256"], offset=pos, frames=len(y),
                           fade_in_samples=fin, fade_out_samples=fout))
        pos += len(y)
    y = np.vstack(parts) if parts else np.zeros((0, ch))
    edges = [0, len(y)] + [e for l in layout if "item" in l for e in (l["offset"], l["offset"] + l["frames"])]
    def extra(z):
        cs = [boundary_check(z, sr, edges, required=a.fade != "none")]
        for k, l in enumerate(layout):
            if "item" in l:
                src = loaded[k][2]; s, n, fi, fo = l["offset"], l["frames"], l["fade_in_samples"], l["fade_out_samples"]
                cs.append(dict(null_check("item_placed_exact", z[s + fi:s + n - fo], src[fi:n - fo]), item=k))
            else:
                seg = z[l["offset"]:l["offset"] + l["gap_samples"]]
                cs.append(check("gap_silent", not np.any(seg), item=k))
        return cs
    o, checks = emit(a.out, y, sr, bits, a.allow_clip, extra)
    params = dict(items=a.items, fade_ms=a.fade_ms, fade=a.fade, allow_clip=a.allow_clip)
    return finish(manifest_for(a.out), "arrange", params, list(sources.values()), [dict(o, layout=layout)], checks)

def verify_manifest(path):
    """Does the manifest still describe the artifacts on disk?"""
    m = json.load(open(path))
    checks = [check("manifest_self_passed", m.get("passed", False))]
    for role in ("sources", "outputs"):
        for e in m[role]:
            if role == "outputs" and not e.get("written", True):
                continue
            p = e["path"] if os.path.isabs(e["path"]) else os.path.join(os.getcwd(), e["path"])
            if not os.path.exists(p):
                checks.append(check(f"{role[:-1]}_exists", False, path=e["path"]))
                continue
            d = describe(p)
            diffs = {k: [e[k], d[k]] for k in ("sha256", "frames", "sample_rate", "channels", "bits") if e.get(k) != d[k]}
            checks.append(check(f"{role[:-1]}_matches_manifest", not diffs, path=e["path"], differences=diffs))
    return checks

def op_verify(a):
    checks = verify_manifest(a.manifest)
    ok = all(c["passed"] for c in checks)
    print(json.dumps(dict(passed=ok, manifest=rel(a.manifest), failed=[c for c in checks if not c["passed"]])))
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(prog="sample_op", fromfile_prefix_chars="@", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    def common(sp, fade="auto"):
        sp.add_argument("--fade-ms", type=float, default=DEFAULT_FADE_MS, help="edge fade length (default %(default)s)")
        sp.add_argument("--fade", choices=("auto", "always", "none"), default=fade,
                        help="auto: fade only edges that are not already silent (default %(default)s)")
        sp.add_argument("--allow-clip", action="store_true", help="permit output beyond full scale (recorded)")
    s = sub.add_parser("slice"); s.add_argument("src"); s.add_argument("--cuts"); s.add_argument("--ranges")
    s.add_argument("--out-dir", required=True); s.add_argument("--prefix", required=True); common(s)
    s.set_defaults(fn=op_slice)
    r = sub.add_parser("reverse"); r.add_argument("src"); r.add_argument("--out", required=True); common(r)
    r.set_defaults(fn=op_reverse)
    q = sub.add_parser("repitch"); q.add_argument("src"); q.add_argument("--out", required=True)
    q.add_argument("--semitones", type=float, required=True)
    q.add_argument("--max-denominator", type=int, default=MAX_DENOMINATOR)
    q.add_argument("--max-cents", type=float, default=0.05); common(q)
    q.set_defaults(fn=op_repitch)
    g = sub.add_parser("arrange"); g.add_argument("--out", required=True)
    g.add_argument("items", nargs="+", help="WAV paths and gap:<time> entries, in order"); common(g)
    g.set_defaults(fn=op_arrange)
    v = sub.add_parser("verify"); v.add_argument("manifest"); v.set_defaults(fn=op_verify)
    a = p.parse_args(argv)
    return a.fn(a)

if __name__ == "__main__":
    sys.exit(main())
