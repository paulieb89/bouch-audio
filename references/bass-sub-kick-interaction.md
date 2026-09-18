# Bass, sub and kick interaction

Shared by `electronic-production` (designing the bass and kick) and
`mixing-and-mastering` (resolving them in a mix). Tier tags follow
`evidence-status.md`.

## Sub design — BOTH

- A convincing sub is harmonically **simple** (sine or triangle). Detuned
  or unison oscillators on the sub voice itself cause beating: the
  fundamental's level fluctuates and reads as an unstable low end.
  [SOURCE-BACKED: Senior, *Sound on Sound* "Mixing Bass"; SOS sub-bass Q&A]
- Keep sub content mono. Width or phase differences below roughly
  100–120 Hz lose level and stability on mono playback (club PA, phone).
  [SOURCE-BACKED, as above]
- The principle is broader than "bass must be mono". Critical low-frequency
  information has to stay predictable when summed and played on different
  systems, and width is frequency-dependent, not a global setting.
  [SOURCE-BACKED: V2 corpus §14]
- **Separate sub function from audibility function.** A low fundamental
  gives weight but disappears on small speakers. Harmonics from
  saturation/distortion let the ear place the bass higher up (the "missing
  fundamental" effect). Structure: **clean mono sub + separately processed,
  harmonic mid-bass**. [SOURCE-BACKED: V2 corpus §6, V1 bass playbook
  sources] [PROJECT-PROVEN as a construction: V2 `designed-sound-palette-01`
  built exactly this split (sine sub + distorted unison mid-bass, separate
  instances), and the palette passed a human verdict]

## Weight comes from discipline, not loudness — BOTH

- **PROJECT-PROVEN (V1 Study 3, human verdict).** In a sparse half-time
  arrangement, convincing darkness and weight came from frequency and
  arrangement discipline: a clean sub, restrained mid-bass, and real
  negative space (measured ~18–20 dB dips in the breath bars). Loudness and
  distortion were not the source.
- The same claim recurs independently in three V1 documents (LAB).
- A moderate duck (2–3 dB against the kick), separate frequency pockets for
  kick and bass, and saturation instead of aggressive EQ boosts are the
  cited mechanisms. Deeper ducking is reported to start sounding odd.
  [SOURCE-BACKED for the 2–3 dB figure; not measured internally]

## Kick vs bass: decide the relationship before processing — BOTH

Do not reach for a sidechain compressor just because two tracks contain
bass. First decide which element owns which job. The V2 corpus (§7,
SOURCE-BACKED) orders the options from least to most destructive:

1. **Rhythmic separation**: don't trigger them together.
2. **Spectral separation**: one owns the deepest region, the other carries
   upper punch.
3. **Temporal separation**: shorten the kick or bass decay.
4. **Phase alignment**: repair destructive interaction.
5. **Dynamic separation**: briefly duck one from the other.
6. **Dynamic spectral separation**: duck only the conflicting band. Dynamic
   EQ does less collateral damage than full-band sidechain compression when
   only a region needs space.

Documented engineer practice treats kick and bass as effectively one
instrument and decides which carries the deeper energy [SOURCE-BACKED:
engineer commentary cited in V2 corpus §7].

**Applied internally (V2 `bass-music-sketch-16bar`): VERDICT PENDING.**
Kick and 808/wobble bass were placed in call-and-response (bass notes in
the gaps between kick hits) instead of building a sidechain. This was the
first option above, chosen as least destructive. The render was technically
clean after gain fixes, but the source records no human verdict on the
committed version. Treat it as a demonstrated *application*, not a proven
musical result.

### An 808 is kick, bass, or both — SOURCE-BACKED

A tuned long-decay 808 can act as bassline and sometimes replaces the kick
[Roland]. Decide which role it plays; that changes everything downstream
(tuning, decay versus note length, distortion, relationship to any kick).

## Layered bass: one anchor — SOURCE-BACKED

When several bass sources stack, choose **one** as the low-end anchor and
high-pass the others (around 100 Hz). Overlapping long-wavelength content
from two sources cancels by phase, and it can reinforce on one note while
cancelling on another. Useful controls: oscillator start phase
(deterministic vs random), time alignment, polarity, summed-waveform
inspection, and rendering several phase relationships to compare. [V2
corpus §3; SOS] [NOT YET demonstrated internally: no polarity/phase
experiment exists]

## Measured pitfall: sub-heavy sources stack — PROJECT-PROVEN

V2's first bass-music render clipped (+1.29 dBTP, 310 clipped samples),
with 81% of energy in 20–60 Hz. Measuring the raw sources showed why: kick
samples, 808 and riser were each 65–99% sub, so three "different" parts
were competing for one band. Measure raw sources when a low end clips or
feels bloated before you reach for processing (`audio-verification`).

## Bass movement — see `sound-design-fundamentals.md`

Reese beating and filter-LFO wobble are different mechanisms (BOTH).
Details are in the sound-design reference.

## Failure modes

- Unison or detune on the sub voice itself.
- Two full-range bass layers with no high-pass split.
- Distorting the sub instead of a separate mid layer.
- A wide or phase-inconsistent sub that collapses in mono.
- Sidechain as a reflex instead of a decided relationship.

## Diagnostics (SOURCE-BACKED, V2 corpus §20)

| Symptom | Investigate first |
|---|---|
| Weak sub | Phase cancellation, wrong register, short decay, stereo cancellation |
| Kick disappears | Masking, weak transient, bass overlap, phase |
| Bass audible only on subs | Not enough upper harmonics |
| Master clips | Low-frequency energy piling up across parts/buses, uncontrolled transients |
