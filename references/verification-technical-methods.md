# Technical verification methods

What deterministic checks can prove about audio, and how to make them
trustworthy. Tier tags follow `evidence-status.md`. The authority boundary
(measurement diagnoses, listening approves) is in
`perceptual-judgment-protocol.md`. Read both.

## Never trust a tool's own success report — BOTH (three sources, independently)

A tool returning success proves the call returned. It does not prove the
state or the audio is what you intended. Re-derive the result from the
artifact:

- **V1:** mutation calls echoed success while the underlying state was
  wrong. The practice became: re-read state after every mutation.
- **V2:** envelope automation that round-tripped perfectly in the project
  file had **no effect** on the rendered audio. Only measuring the signal at
  the automated moments revealed it. A sampled instrument whose load
  "succeeded" rendered correct audio, silence or garbage across repeated
  renders, because it was still loading asynchronously. Practice: render
  twice and compare when state may not have settled.
- **V2:** a reverse tool was verified by the reversed file's RMS envelope
  (the start/end of the output matching the end/start of the input), not by
  its exit code.
- **RMCP:** inspect before mutating and preview before applying, as an
  eval-enforced ordering (`preexisting_master_chain`).

General health checks (loudness, clipping, silence) do **not** confirm that
a *specific intended effect* happened. To confirm an effect, measure the
signal where and when the effect should be.

## Standard render measurements — BOTH (tooling proven; BS.1770 is an ITU standard)

`tools/analyze.py` reports, as JSON: duration, BS.1770-4 integrated
loudness, max short-term loudness, loudness range (LRA), sample peak, true
peak (4× oversampled), clipped-sample count, stereo correlation, side/mid
ratio, spectral centroid, six band-energy percentages (sub 20–60, bass
60–150, low-mid 150–400, mid 400–2k, hi 2k–6k, air 6k–20k), and silence
runs ≥ 0.5 s. `--sections` adds per-section short-term loudness;
`--window START DUR` runs the same suite on a slice.

The loudness meter reproduces the ITU-R BS.1770 reference filter and
matches ffmpeg `ebur128` on real renders. The V1/V2 original read slightly
low (0.05–0.09 LU on mixes, ~0.25 LU on a 1 kHz tone) and was corrected
here, so treat absolute loudness figures quoted in V1/V2 records as
marginally low. The tests check each detected fault class against a signal
that must trip it.

Check for things that are **wrong**, not for whether the music is good:

- duration matches the intended length;
- no clipped samples, and a sensible true peak (measure it; see
  `mastering-boundaries.md` for the −2 dBTP safety convention);
- no unintended silence (a silent part, a missing file, an unsaved
  project);
- no large band or stereo anomaly the brief doesn't explain (a vanished
  sub, a mono-collapsed pad, 80% of energy in 20–60 Hz);
- loudness-matched versions before anyone compares them.

Interpreting results (PROJECT-PROVEN cases):

- Band energy is energy-weighted and naturally biased toward the low end.
  A sustained sine sub produced 70% in `sub_20_60` in a mix that was fine.
  An 81% reading in another sketch traced to sources that were genuinely
  too sub-heavy. The number starts an investigation; it is not a verdict.
- Section loudness and LRA confirm that an intended dynamic arc actually
  landed (V1 Study 5: monotonic rise vs a 12 dB dip). They cannot say
  whether it lands musically.

## Measure the right window — PROJECT-PROVEN (V2 FM case)

Whole-file aggregates cannot see short events. A 2-operator FM bell showed
**no** whole-file difference with the modulator on or off. A 21 ms attack
window showed centroid ~2980 Hz decaying to ~724 Hz with the modulator,
against ~420 Hz flat without it. For attack, transient or onset questions,
measure a window around the event:

```
analyze.py render.wav --window 0.0 0.021
```

Short windows correctly return `null` for integrated loudness and LRA,
because a window that short cannot support them.

## Isolate the defect with a static control — PARTIAL (one source, generalises)

When a specific feature seems not to work in a pipeline, build a **minimal
static control on the identical path** before concluding anything. In V2,
the automation that disappeared from renders (above) could have been a
general gain or render fault. A static volume change on the same path
dropped loudness by the expected ~26 LU, which isolated the defect to
automation specifically. This applies to any render/bounce/export pipeline.

## Prove offline transforms with manifests and seeded faults — PROJECT-PROVEN (V1)

For any tool that edits audio offline, don't spot-check. Prove its
postconditions and prove the checks themselves can fail:

- **Known input**: a generated or fixed signal, not "some render".
- **Postconditions read back from disk**: all samples finite; nothing past
  full scale unless explicitly allowed and recorded; the file reopens with
  the intended format and length; exact nulls where the operation should be
  exact (a slice region equals its source; reverse equals x[n−1−i];
  reversing twice gives the identity); lengths match the ratio;
  arrange gaps are digital silence.
- **Click detection at every created boundary**: peak |second difference|
  at the boundary over the median of the busier neighbouring 10 ms. It
  counts as a click above ratio 8 and above 1e-3 absolute. Calibrated on
  four material types: hard cuts were caught 100% on sustained material and
  45% on broadband noise. The detector is weaker in noise, and it only looks
  at created boundaries.
- **Manifest** beside every output: operation, parameters, source and
  output sha256, frames, rate, channels, bits, and every check with its
  measured values. `verify` re-hashes everything later.
- **Seeded faults**: V1 planted 12 faults (a hard cut, a one-sample spike at
  a junction, an off-by-one slice boundary, one changed LSB, a truncated
  output, resampling overshoot, NaN, a truncated WAV, a post-manifest edit,
  a too-coarse ratio denominator) and confirmed each was caught by a named
  check. A null result from a checker that has never caught a planted fault
  is not evidence.

`tools/sample_op.py` implements this. `tests/test_sample_op.py` carries the
seeded-fault suite. For a *new* tool, apply the pattern in proportion: a
known input, a seeded positive and negative, and inspection of the real
output. Add hashes/manifests when the tool's correctness depends on
exactly which bytes it read (V2 tools README).

## Behavioural evals for an agent's discipline — SOURCE-BACKED pattern (RMCP)

Epistemic rules for an audio agent can be tested deterministically: score
captured tool traces with binary rules (forbidden tools, required tools,
required call order, required or forbidden phrases in the final response).
Don't use an LLM judge, and don't claim to measure taste. RMCP has 9 such
mastering-safety cases (listed in `mastering-boundaries.md`). The pattern
generalises; RMCP's specific tool lists do not.

## Linear-media delivery

For audio delivered with picture, the same discipline holds at file level:
probe the container/stream spec, measure integrated loudness against the
delivery target, and detect silence and clipping on the *delivered* file.
Checking whether audio events land on picture events needs onset detection
against the intended timestamps. V1 proposed that but never built it. It is
a gap with no calibrated tolerance.
