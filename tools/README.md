# Deterministic audio tools

Two offline, DAW-independent tools, promoted because they have tested,
evidenced behaviour. Both report **technical** postconditions only. Neither
can say whether audio sounds good.

Dependencies: Python ≥ 3.10, numpy and scipy. Each script carries PEP 723
inline metadata, so `uv run tools/<script>.py …` resolves dependencies by
itself. Otherwise use any interpreter that has numpy and scipy installed.
Tested with numpy 1.26.4 / scipy 1.16.3 and numpy 2.5.3 / scipy 1.18.1
(see `evidence/qualification.md`).

## `analyze.py`: render measurement

```
analyze.py render.wav                              # whole-file JSON report
analyze.py render.wav --window START_S DURATION_S  # same metrics on a slice
analyze.py render.wav --sections sections.json     # + per-section loudness
```

Reports: duration, BS.1770-4 integrated loudness, max short-term loudness,
LRA, sample peak, true peak (4× oversampled), clipped samples (|x| ≥
0.9999), stereo correlation, side/mid ratio, spectral centroid, six
band-energy percentages, and silence runs ≥ 0.5 s at −60 dBFS.
`sections.json` is `[["name", start_s, end_s], ...]`.

- Input: PCM WAV, 16/24/32-bit integer. Float WAV is rejected by Python's
  `wave` module; convert it first.
- A window too short for BS.1770 gating returns `null` for
  `lufs_integrated` / `lra_lu`. That is correct, not a failure.
- Exit 2 on bad arguments or an out-of-bounds window.

Provenance: V2 `tools/analyze.py` at `bc460db`, ported from V1's
implementation. Changes made when promoting it:

- **K-weighting corrected.** The V1/V2 filters fed libebur128's design
  parameters into a different (RBJ cookbook) biquad formula. As a result,
  integrated/short-term loudness read about 0.25 LU low on 1 kHz-centred
  material and 0.05–0.09 LU low on real mixes. The filters now reproduce
  the ITU-R BS.1770 48 kHz coefficients to machine precision and agree with
  ffmpeg `ebur128` to within its 0.1 LU display rounding on eight real
  renders (`evidence/qualification.md`). Loudness figures recorded in V1/V2
  documents carry that small low bias. Comparisons between renders made
  with the same meter are essentially unaffected.
- Known-positive tests added for the EBU 1 kHz reference level, clipping,
  inter-sample true peak, silence runs and mono cancellation, after a
  mutation run showed the inherited suite could not catch a broken clip
  detector.
- Portable shebang, PEP 723 inline dependency metadata, and a `np.trapz` →
  `trapezoid` fallback (deprecated in numpy 2).

Known quirk (inherited, unchanged): identical L/R channels give
`side_mid_ratio_db` = `-Infinity`, which Python's `json` emits as a
non-standard token.

## `sample_op.py`: verified offline sample operations

```
sample_op.py slice   SRC --cuts 0.5s,0.75s        --out-dir D --prefix NAME
sample_op.py slice   SRC --ranges 0.5s-0.6s,2s-2.1s --out-dir D --prefix NAME
sample_op.py reverse SRC --out OUT.wav
sample_op.py repitch SRC --semitones -5 --out OUT.wav          # varispeed: duration changes
sample_op.py arrange --out OUT.wav a.wav gap:250ms b.wav        # or @items.txt
sample_op.py verify  MANIFEST.json
```

Times are `<n>s`, `<n>ms` or a bare sample count. Fades default to `auto`
(3 ms raised cosine, only on edges that are not already silent);
`--fade none` is the control path. Output is 24-bit PCM (32-bit for 32-bit
sources).

Every operation reads its own output back from disk, runs its checks and
writes `<out>.manifest.json` (operation, parameters, source/output sha256
and format, every check with measured values, `passed`). Exit 0 means every
required check passed; exit 1 means the manifest names the failure.
`verify` re-hashes sources and outputs later. Manifest paths are relative
to the working directory the tool ran in, so run `verify` from the same
directory.

Not available: overlap/layering, crossfades or per-item gain in `arrange`;
duration-preserving repitch/stretch; onset detection; zero-crossing snap;
float WAV; sample-rate conversion between items.

It imports `read_wav` from `analyze.py`, so keep the two files together.

Provenance: V1 `sample_op.py` at tag `v1-evidence-freeze-2026-09-13`
(sha256 prefix `c16a3f6e96eefaa2`, matching V1's frozen record). Changes
made when promoting it: manifest paths relative to the working directory
instead of the V1 repository root, portable shebang, inline dependency
metadata.

## Tests

```
python -m pytest tests/
# or, with nothing installed:
uv run --no-project --with numpy --with scipy --with pytest python -m pytest tests/
```

The suites use generated signals and seeded faults only. Two optional
checks run against real material when pointed at it:

- `SAMPLE_OP_REAL_MATERIAL=<sustained stereo PCM WAV>`: hard cuts on real
  sustained material are flagged, and faded cuts pass.
- `ANALYZE_BELL_RENDERS=<dir with bell_test_op2off.wav, bell_test_algo5.wav>`:
  the original V2 FM-transient renders.

Neither the V1 source sample nor the V2 renders are redistributed.
