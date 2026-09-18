# Arrangement, builds, drops and movement

Tier tags follow `evidence-status.md`. Linear-media users: the same
contrast mechanics apply to a reveal or cut. The mapping onto picture is
the consumer's call and is HYPOTHESIS until it has been listened to.

## Arrival is contrast, not loudness — BOTH

- A drop registers as impact because of what came before it. Narrowing or
  thinning the build (less width, sub held back) makes the return of full
  range and width land as arrival. [SOURCE-BACKED: SOS "Classic
  Stereo-widening", convergent trade practice]
- A drop can carry **two** contrast events: the hit, then briefly dropping
  kick/bass/lead for about a bar before the full pattern returns.
  [SOURCE-BACKED]
- Stereo width is an arrangement device, not only mix polish. Pull an
  element narrow in one section and open it in the next. Band-split
  widening stays mono-safe; polarity-trick widening can cancel in mono.
  [SOURCE-BACKED: SOS]

## Builds combine additive and subtractive movement — BOTH

- Additive: rising density (snare roll) together with a filter opening,
  revealing the top end in step. Subtractive: strip to a skeleton, then
  reintroduce. Most convincing builds use both. [SOURCE-BACKED: Attack
  Magazine "10 Snare Rolls For The Drop"]
- **PROJECT-PROVEN as mechanisms (V1 Study 5).** An additive build and a
  subtractive-then-arrival build were tested against the identical drop.
  Section loudness confirmed both did what they were built to do: a
  monotonic rise versus a genuine 12 dB near-silence dip. The drops landed
  within 0.06 LU of each other. **The listener preferred additive for that
  material only.** Which one arrives harder depends on the material; it is
  not a ranking.

## Transition alternatives to a generic riser — SOURCE-BACKED; PARTIAL internally

- **Reversed organic material**: bounce a short existing part (a stab, fill
  or ad-lib), then reverse, stretch and filter-sweep it. It reads as a riser
  with more character than synthesised noise.
  **PROJECT-PROVEN as a construction (V2):** a reversed-drone riser timed to
  peak on the drop downbeat. Its correctness was verified by RMS-envelope
  symmetry rather than the tool's exit code (see `sample-transformation.md`).
  That sketch's musical verdict is PENDING. The reverse-into-ring-mod
  texture riser in `designed-sound-palette-01` is part of a palette that
  passed.
- **Silence before impact**: near-silence right before a hit is an active
  tension tool, not dead air. [SOURCE-BACKED] V1 Study 5's subtractive build
  measured it (a 0.55 s silence run) [PROJECT-PROVEN as a mechanism].
- **Tempo-synced modulation** (gating, tremolo, ducking) on the transition
  element ties it to the groove [SOURCE-BACKED].
- **Breakdown → rebuild** is an energy reset. Keeping the same skeletal part
  but changing its voicing or patch makes it recognisable yet heard
  differently. [SOURCE-BACKED, convergent convention]

## New material beats more density — PROJECT-PROVEN

Concrete Bells V0's final section tried to feel bigger by adding layers and
volume. The V1 fix was harmonic development (an apex progression), not
more drums, and the listener accepted it. "It needs to feel bigger" is not
automatically a request for density. [V1 `concrete-bells-v1`]

## Repeated harmony without staleness — PARTIAL

Two genuinely different mechanisms [SOURCE-BACKED: Attack Magazine, "Four
Tet – Angel Echoes" breakdown], with one internal instance [PROJECT-PROVEN:
V1 Concrete Bells final section]:

1. **Reharmonise** one chord inside a fixed progression (e.g. major →
   major 7th, or a common-tone substitution).
2. **Rhythmic displacement**: leave the harmony alone and change where it
   lands. The documented example splits a progression into asymmetric
   7-beat/5-beat phrases so the tonic never lands on the bar line.

Melody writing in general is thin: NOT YET COVERED beyond this.

## Movement at three time scales — SOURCE-BACKED (V2 corpus §19)

| Scale | Examples |
|---|---|
| Micro | Transient variation, small pitch movement, velocity, random modulation |
| Phrase | Fills, delay throws, filter motion, reverses, risers |
| Section | Widening, filters opening, distortion changing, bass removed, reverb space changing |

"The second eight bars feel static" should first prompt a change of timbre,
density, width, depth, rhythm or transient behaviour, not another melody.

### Movement without host automation — PROJECT-PROVEN (V2)

Timeline automation was never reliably rendered in the V2 pipeline. Two V2
pieces nonetheless got convincing movement from:

- patch-internal modulation (filter envelopes, LFOs, unison beating, an
  ensemble/chorus stage inside the synth);
- note-level velocity shaping written into the notes;
- structural on/off contrast between sections.

`designed-sound-palette-01` built its movement this way and passed its
human verdict. Note that the listener credited the *evolving pad* in
particular.

**Automation as composition** (sweeping filters, sends or width to mark
sections) is SOURCE-BACKED (V2 corpus §15, citing documented engineer
practice). It was **never demonstrated** internally, because the V2 render
path dropped envelope automation. It remains a gap, not a disproof.

## Failure modes

- A build that is only additive (riser + density), heard as one long
  crescendo.
- A drop that is "everything, louder" with no preceding contrast.
- Density used to solve an ending that needed new material.
- The same generic noise riser on every transition.
- One loop pattern and one modulation setting for the whole track.
