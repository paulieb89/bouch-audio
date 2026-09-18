# Rhythm, groove and drums

Tier tags follow `evidence-status.md`. This is the best-tested production
area in the package.

## Human feel is structured, not random — BOTH

- Randomising timing and velocity uniformly reads as noise, not groove.
  Convincing variation follows musical logic: planned accents, per-role
  offsets, and phrase shape. On top of that sits only a thin random layer, in
  the order of ±4 velocity. [SOURCE-BACKED: Anderton, *Sound on Sound*,
  "Secrets of Expressive Sequencing" / "Programming Realistic Drum Parts"]
- **PROJECT-PROVEN, twice, independently (V1).** Concrete Bells V0 had
  velocity variation that was statistically present but structurally
  meaningless, and a listener heard it as "noticeably mechanical". V1 rebuilt
  the drums with structural humanisation and was heard as much less robotic.
  A second, much sparser 140 BPM groove built the same way was judged
  convincing (V1 Study 2). The one remaining weakness was sample choice, not
  timing.

The V1 construction, as numbers you can start from (not targets):

| Role | Treatment in Concrete Bells V1 |
|---|---|
| Kick | ±2 ms scatter only. The low end stays anchored. |
| Backbeat snare | Laid back a fixed +7 ms |
| Ghost notes | Anticipate at −3 ms |
| Hats | Structural 16th swing (fixed offset on odd 16ths, a smaller one on off-beat 8ths), plus small scatter |
| Fills | Rush in proportion to position in the roll |
| Velocity | Per-role, per-grid-position base tables × per-bar phrase multiplier × deterministic hand-alternation bias. Random scatter goes on last. |
| Patterns | Kick/snare placement varies by section (e.g. syncopation on alternating bars) instead of looping one pattern |

## Role-dependent tightness — BOTH

Keep the kick (and so the sub) tight. Snare placement is the main feel
lever. Hats and percussion get the most freedom. [SOURCE-BACKED: *Sound on
Sound* sources above] [PROJECT-PROVEN: V1 Concrete Bells, Study 2]

The same principle carries over to bass phrasing: keep the attack tight
against the kick and let sustained modulation be the loose part
[HYPOTHESIS as a bass rule, extrapolated in V1's wobble playbook].

## Swing, ghosts, partial quantise — SOURCE-BACKED

- Swing delays alternate subdivisions. 50% is straight and ~66% is a full
  triplet shuffle. The useful range is roughly 50–75%, narrower (~50–62%) in
  dance practice. It is usually applied selectively, for example to hats,
  not to the whole kit. "Laid back" means late against the grid; "on top" or
  "pushed" means early. [*Sound on Sound*, "Quantisation & Groove Functions
  in Logic"]
- Ghost notes are low-velocity hits in the gaps. They add texture, not
  primary rhythmic information.
- Partial quantisation moves notes a percentage of the way to the grid. It
  tightens a part while keeping its timing character. [SOURCE-BACKED; not
  tried internally]

## Intentionally tight is not a failure

Precisely gridded feel is legitimate where the style calls for it. What V1
evidenced as "mechanical" was *everything* on the same grid with nothing
left to move [PROJECT-PROVEN, V1].

## Functional drum layering — SOURCE-BACKED; PARTIAL internally

- Layer by job, not quantity: sub/weight + body + transient/click +
  character/noise (+ optional space), then remove overlapping content from
  each layer. Attack Magazine calls this "EQ bracketing". Snare: body +
  crack + noise/tail. Hats: transient + metallic/noise texture + room.
  [SOURCE-BACKED: V2 corpus §8, §18; Attack Magazine "Layering Drums"]
- Kick synthesis model: fast downward pitch transient + decaying low
  oscillator + optional click/noise layer [SOURCE-BACKED: V2 corpus §6].
- **Internal evidence is thin and mostly negative.** Every kick sample
  available to V2 was 89–99% sub-band energy with no separate click. Such a
  kick behaves as a second bass voice, stacks with the 808, and caused real
  clipping [PROJECT-PROVEN measurement, V2 `bass-music-sketch-16bar`].
  Choose kick sources for a transient that sits apart from the bass, and
  measure raw sources before mixing them (`audio-verification`).
- A sampled kit with hard velocity layers is not round robin: it changes
  timbre by velocity band, not by repetition. Where true variation is
  needed, alternate between several pre-auditioned samples [PROJECT-PROVEN
  observation, V1].

## Failure modes seen in practice

- Uniform randomisation called "humanisation" (V1 V0).
- One grid for every element, nothing moving (V1 V0).
- Loosening kick and sub along with everything else.
- Adding drum density to fix a section that needed new material (see
  `arrangement-and-movement.md`).

## Not covered

Per-instrument drum *sound design* (what makes a kick, clap or hat good
sonically) and transient-shaper use are NOT YET COVERED. See
`evidence-status.md`.
