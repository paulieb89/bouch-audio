# Sample transformation and resampling

Used by `electronic-production` (resampling as a creative move) and
`audio-verification` (how to prove an offline transform did what it
claims). Tier tags follow `evidence-status.md`.

## Resampling is a first-class production move — BOTH

- Competent electronic production is recursive: generate → process →
  render → chop → pitch → reverse → distort → stretch → render again.
  Treat render/bounce, reverse, crop, split, stretch, transpose and
  replace-with-render as primitive actions, not special cases.
  [SOURCE-BACKED: V2 corpus §12; Bitwig bounce documentation]
- **Keep the original, or a recoverable branch, before any destructive
  transform** [SOURCE-BACKED; applied throughout V1/V2].
- **PROJECT-PROVEN (V2):** a riser made by offline reverse of a drone,
  timed to peak on the downbeat (`bass-music-sketch-16bar`, verdict
  PENDING). Also a reversed impact passed through ring modulation into a
  swelling transitional texture (`designed-sound-palette-01`, palette
  PASS).

## What transforms did for material — PROJECT-PROVEN, provisional (V1 sample-ops v1)

One reversed-vocal wash, rendered as five candidates in one musical context
and judged by one listener, blind and loudness-matched:

- **Slice and rearrange** (unpitched chops rearranged into a syncopated
  2-bar pattern) was preferred. It made the material more useful than
  leaving it untransformed.
- **Varispeed on short pitched chops** read as impact, not as a defect.
  **As a long −12 st bed** it lifted nothing over the untransformed control.
- **Reversed decay swells** into the snare worked as a sparse rhythmic
  device, not only as a transition.
- The untransformed and varispeed beds were both heard as atmospheric
  utility, not hooks.

The source marks these as provisional: one listener, one context, one
source. The verdicts also rate the arrangement choices made with each
operation, not the operations in isolation.

## Duration-preserving repitch is not yet justified — PROJECT-PROVEN reasoning

Every pitched chop in the V1 experiment was cut to grid length *after*
varispeed, so the duration change never broke timing. Varispeed's real
costs are timbral (a formant shift going up; halved internal motion going
down), and only a listener can judge those. Duration-preserving pitch/stretch
becomes necessary with material that has internal timing: speech, loops,
long phrases that must hold a bar. Choose varispeed unless the material has
internal timing.

## Tool in this package

`tools/sample_op.py` (see `tools/README.md`) does slice, arrange with
silent gaps, whole-file reverse, varispeed repitch, edge fades and verify.
Every operation writes a manifest.

Not available: overlap/layering or crossfades in `arrange`;
duration-preserving repitch or stretch; onset detection; zero-crossing snap;
float WAV input; sample-rate conversion between items. If a task needs one
of these, say so; don't pretend the tool covers it.

## Rights and provenance — PROJECT-PROVEN practice

- Record origin and usage rights for every source recording: author, URL,
  licence as shown, date checked, and hash. Keep the transform manifests;
  a chain of manifests (slice → repitch → arrange), each naming its
  source's sha256, *is* the provenance.
- Getting new material and confirming its rights is a human step, not part
  of a creative task.
- Prefer CC0/CC-BY. Check share-alike terms before using material in a
  deliverable.

## Verification

Checking a transform's postconditions (exact nulls, lengths, click-free
boundaries, seeded faults) is covered in
`verification-technical-methods.md`. Those checks prove technical
correctness only. Whether the result is musically useful is a listening
question (`perceptual-judgment-protocol.md`).
