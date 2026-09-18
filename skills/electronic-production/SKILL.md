---
name: electronic-production
description: Evidence-tagged reasoning for making electronic music and sound material that does not exist yet — choosing a synthesis route, designing bass/sub/kick and pads, programming drums with human feel, arranging builds, drops and transitions, adding movement, and resampling or transforming samples (slice, reverse, repitch). Use when designing a sound, writing or humanising drums, arranging or developing a section, scoring or designing SFX, or turning source audio into new material, in any DAW or in code. Not for balancing or processing an existing mix or mastering (use mixing-and-mastering), and not for checking whether a render is correct (use audio-verification).
metadata:
  package: bouch-audio
  evidence: tiered; see references/evidence-status.md
---

# Electronic production

Reason from mechanisms and evidence, not presets. The detailed knowledge
lives in the shared references at the package root. Load only the one the
current decision needs.

## Before building anything

1. **Name the job.** State what the sound or section must do (weight,
   identity, tension, arrival, texture), not what it should be called.
   Build one layer per job; don't stack presets.
2. **Check the evidence tier** of any technique you rely on. Tags come from
   [`../../references/evidence-status.md`](../../references/evidence-status.md).
   A SOURCE-BACKED claim is a hypothesis to render and listen to. A
   PROJECT-PROVEN claim is a strong starting point that still holds only
   for its context. A NOT YET COVERED area is a gap: say so. Do not
   present general knowledge as this package's guidance.
3. **Choose the least-destructive move.** Arrangement and source choice
   come before processing. Keep the original before any destructive
   transform.

## Route to the reference

| Decision | Read |
|---|---|
| Drum programming, groove, swing, humanisation, drum layering | [`../../references/rhythm-groove-drums.md`](../../references/rhythm-groove-drums.md) |
| Sub, 808, bass layering, kick vs bass relationship | [`../../references/bass-sub-kick-interaction.md`](../../references/bass-sub-kick-interaction.md) |
| Builds, drops, transitions, breakdowns, repetition, movement over time | [`../../references/arrangement-and-movement.md`](../../references/arrangement-and-movement.md) |
| Synthesis route, oscillators/unison, envelopes/LFOs, filters, wobble vs Reese, FM, pads | [`../../references/sound-design-fundamentals.md`](../../references/sound-design-fundamentals.md) |
| Resampling, slicing, reversing, repitching, sample provenance and rights | [`../../references/sample-transformation.md`](../../references/sample-transformation.md) |

## Boundaries with the other Skills

- **Built vs balanced.** If the material does not yet exist as committed
  audio, it belongs here. If it exists and is being balanced, diagnosed or
  compared, use `mixing-and-mastering`. Saturation straddles the line: a
  distortion stage inside a patch is sound design, and saturation on a
  track or bus is mixing. Decide by which one you are doing.
- **Proving it works.** After any render, bounce or transform, use
  `audio-verification`. It covers the tools in `../../tools/`
  (`analyze.py`, `sample_op.py`) and the listening protocol.
- **Listening decides.** No technique here is "done" because it measured
  well or matched a reference. Timbre, feel and whether it works are a
  human listener's verdict.

## Deliberately not here

DAW or plugin operation (track, FX and patch-loading mechanics), sample
libraries, and dated genre or scene vocabulary. Use whatever
project-local adapter, tool or workbench the environment provides for
operation; this Skill supplies the reasoning.
