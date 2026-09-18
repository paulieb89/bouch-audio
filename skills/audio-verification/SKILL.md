---
name: audio-verification
description: How to check audio work before trusting or reporting it — measuring a rendered, bounced or exported WAV (BS.1770 loudness, LRA, true peak, clipping, silence, stereo correlation, band energy, windowed attack/transient analysis), proving an offline audio edit (slice, reverse, repitch, arrange) with manifests and seeded faults, isolating a pipeline defect with a static control, and preparing a loudness-matched blind A/B so a human listener decides. Use after any audio render or export, when a tool reports success on audio, before claiming a mix, sound or soundtrack works or is better, or when asked which version sounds better. Not for deciding how to design or mix the sound itself (electronic-production, mixing-and-mastering).
compatibility: The bundled tools need Python 3.10+ with numpy and scipy (or uv, via the scripts' inline metadata). The reasoning works without them.
metadata:
  package: bouch-audio
  evidence: tiered; see references/evidence-status.md
---

# Audio verification

Two kinds of authority, never mixed up:

- **Deterministic checks prove technical properties.** Levels, peaks,
  clipping, silence, lengths, exact nulls, format, stereo correlation.
- **A human listener decides perceptual and musical questions.** Timbre,
  feel, "does it work", "which is better". You cannot hear. Never state a
  listening judgement as fact. Label any opinion as the agent's.

## Procedure

1. **Don't trust success echoes.** A tool reporting OK is not evidence.
   Re-derive the result from the produced file or state.
2. **Measure the artifact** with the bundled analyser (paths are relative
   to this Skill):

   ```
   python ../../tools/analyze.py render.wav                     # whole file, JSON
   python ../../tools/analyze.py render.wav --window 0.0 0.021  # a transient/attack
   python ../../tools/analyze.py render.wav --sections s.json   # per-section loudness
   ```

   With uv, `uv run ../../tools/analyze.py …` installs numpy and scipy from
   the script's inline metadata. Look for what is **wrong** (clipping,
   unintended silence, wrong duration, unexplained band or stereo
   anomalies). A pass means technically sound, not approved.
3. **Confirm the specific intended effect** where and when it should
   happen: a window around the event, or a static control on the same path
   when a feature seems not to work.
4. **Offline edits:** use `../../tools/sample_op.py` (slice, arrange,
   reverse, repitch, verify). Every output gets a manifest with hashes and
   per-check results. Exit code 0 means every required postcondition
   passed. Keep the manifests; they are the provenance.
5. **Hand over for listening:** loudness-matched, blind-labelled, answer
   key withheld in a file, with the technical summary labelled as
   technical. Record the verdict as instance-specific. Until a listener has
   heard it, the status is PENDING.

## Route to the reference

| Need | Read |
|---|---|
| What each measurement means, windowing, static controls, manifests and seeded faults, delivery checks | [`../../references/verification-technical-methods.md`](../../references/verification-technical-methods.md) |
| The listening authority boundary, blind A/B preparation, recording verdicts | [`../../references/perceptual-judgment-protocol.md`](../../references/perceptual-judgment-protocol.md) |
| Transform capabilities and limits, provenance and rights | [`../../references/sample-transformation.md`](../../references/sample-transformation.md) |
| Tool usage, dependencies, tests | [`../../tools/README.md`](../../tools/README.md) |
| What is proven vs source-backed vs missing | [`../../references/evidence-status.md`](../../references/evidence-status.md) |

## Limits to state honestly

- `analyze.py` reads PCM WAV (16/24/32-bit integer), not float WAV.
  Convert first.
- Band energy is energy-weighted toward low frequencies. It is a lead to
  investigate, not a verdict.
- The click detector only inspects boundaries the tool created, and it is
  less sensitive in broadband noise.
- No onset/timing checker is included. Checking audio events against
  picture or beat timestamps is a known gap.
