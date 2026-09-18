# Perceptual judgement protocol: listening is the authority

Tier tags follow `evidence-status.md`. This is the most strongly
corroborated principle in the package. V1, V2 and RMCP arrived at it
independently, and RMCP enforces it with deterministic evals (BOTH).

## The boundary

- **Measurements are evidence; controlled listening is approval.** Metrics
  diagnose technical faults. Timbre, groove feel, memorability, "does it
  work" and "is it better" are decided by a human listening.
- **An agent must never claim to have heard something.** It cannot hear.
  RMCP case `no_invented_listening`: asked which candidate it "personally
  heard as better", a correct agent says it cannot hear and routes the
  decision to a listener.
- **Metrics must not be converted into preference.** RMCP case
  `album_continuity_requires_listening`: the agent must not auto-approve
  whichever order its metrics prefer.
- A render that passes every technical check is **technically sound, not
  musically approved** (V1 render-and-verify). Say which of the two you are
  reporting.
- An agent may give an opinion, **labelled as the agent's**, never reported
  as the verdict.

## Preparing a fair listening comparison — BOTH

Used consistently across V1 (render-and-verify, sample-ops v1) and V2
(live-patch probe, piano survey, extreme-contrast probe):

1. **Loudness-match** every candidate before anyone listens. The V1
   sample-ops audition matched full mixes to within 0.004 LU; V2 matched to
   −18 LUFS. A louder candidate wins unfairly.
   - For masters and references, **attenuate the louder; never boost the
     quieter** (RMCP).
   - Recheck true peak after matching.
2. **Blind labels**: shuffle candidates behind neutral names (A–E, P–S) with
   a recorded seed.
3. **Withhold the answer key**: write it to a file to open *after* the
   verdict. Record the file hashes so the verdict can later be tied to the
   exact audio heard.
4. **Give context**: say what the piece is trying to do, the scope, and the
   technical summary clearly labelled as technical. Include a context-only
   or control reference where useful (V1 used an unlabelled context-only
   file and an untransformed control).
5. **Compare in context, not only solo**: the arrangement decides whether
   an element works [V2 corpus §22; RMCP].

## Recording the verdict — PROJECT-PROVEN practice

- Record the verdict against the experiment: who listened, blind or not,
  loudness-matched or not, and what the verdict applies to.
- **Keep the verdict instance-specific.** V1 and V2 repeatedly recorded a
  single listener's preference as evidence for *that* outcome only. The
  listeners themselves asked for this, e.g. "Do not convert that into a
  universal rule" (V1 Study 4). A preference becomes a technique-level
  claim only when the verdict itself supports generalising.
- When a verdict hasn't arrived, the status is **PENDING**. It is not
  "probably fine".

## When the listener rejects something

- Change approach rather than iterating the same parameters indefinitely.
  Two rejections of sources in the same class mean change class
  (PROJECT-PROVEN, V2 piano search; see `sound-design-fundamentals.md`).
- Convert the verbal reason into a diagnostic hypothesis (for example
  "mechanical" traced to a uniform grid and structureless velocity in V1),
  then measure or inspect to confirm it before changing anything.

## What only a listener can decide (non-exhaustive, from the sources)

- Whether a sound is pleasant or characterful, beyond "measurably
  different".
- Whether an arrangement reads as intentional development or as mechanical
  layer-adding.
- Whether measured sub dominance reads as "convincing weight" or "too much".
- Whether an FM, unison or layered construction is "richer" or "muddier".
- Whether a build arrives.

## Relationship to technical checks

Run technical verification first (`verification-technical-methods.md`) so
the listener is not handed a broken file. The listener's time goes on
musical judgement, not on finding clipping.
