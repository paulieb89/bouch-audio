# Mixing: dynamics, tone, saturation, space and gain

Tier tags follow `evidence-status.md`. Much of this reference is
SOURCE-BACKED doctrine that has not been re-demonstrated internally. It is
marked so that a claim built on it gets rendered and listened to before it
is reported as working.

## Before any processor: name the problem — SOURCE-BACKED (RMCP, canon-attributed)

Before a consequential change, be able to answer these (adapted from the
RMCP action-admission test, attributed there to Senior, Katz and
Shepherd):

1. What specific problem is being solved?
2. What evidence shows it exists? (A measurement, or a listener's report.)
3. Where does it occur: which source, section or time range?
4. Is an earlier-stage fix available (arrangement, performance, source
   choice, level)?
5. What is the smallest reversible action likely to solve it?
6. How will the result be compared level-matched?
7. Who approves the result by listening?

If an answer is missing, inspect, measure or ask instead of processing.
The static balance (levels, pan, mutes, arrangement, no processing) is the
**control condition** for every later A/B.

### Escalation order — SOURCE-BACKED (RMCP)

Move to the next response only when the earlier one cannot fix the problem
without damage:

| Problem | First response | Then, if evidence remains |
|---|---|---|
| Phrase level jumps | Clip gain / local automation | Compression for the remaining envelope |
| Element buried | Level, timing, arrangement, pan | EQ; then narrow, keyed dynamic reduction |
| Mud or resonance | Identify the source and moment | Small static or dynamic EQ move |
| Section lacks movement | Arrangement and rides | Effect throws, return automation |
| Mix lacks width | Arrangement and pan | Source-specific stereo treatment + mono check |
| Mix lacks impact | Balance and transient relationships | Bus dynamics, only for a confirmed envelope problem |

## EQ — SOURCE-BACKED only

- Static EQ fixes a relationship that is *always* wrong. Dynamic EQ fixes
  one that goes wrong only under certain conditions. Sidechain dynamic EQ
  removes part of one source's spectrum only when another source needs it.
  [V2 corpus §11; FabFilter documentation]
- A spectrum analyser showing overlap is **evidence of possible masking,
  not proof**. Instruments are allowed to share frequencies. [V2 corpus §11]
- An EQ move needs a location and a symptom. Never copy frequencies from a
  reference song. [RMCP]
- No internal measured before/after exists for EQ decisions (a known gap).
  Static high-passes on pads/leads/hats to keep them out of the bass band
  were used in V2 sketches as ordinary hygiene. That was not tested as a
  claim.

## Compression — SOURCE-BACKED (arrangement-first avoidance applied internally, VERDICT PENDING)

- Choose compression for a **stated envelope/dynamics job**, never because
  a track type "needs compression". Jobs [V2 corpus §10]: peak control,
  sustain/body, transient shaping (via attack/release), glue, pumping,
  ducking, parallel density. Attack, release and detector behaviour matter
  at least as much as threshold/ratio.
- Two compressors in series need two different named jobs. Level-match the
  bypass comparison: louder is not better. [RMCP]
- Often the right answer is **not compressing**. See the arrangement-first
  sidechain decision in `bass-sub-kick-interaction.md` (applied in V2;
  verdict pending).
- Sidechain *compression pumping* was never achieved end to end internally
  (a gap).

## Saturation, distortion, clipping — BOTH

- Treat them as three operators [SOURCE-BACKED, V2 corpus §9]. **Saturation**
  is progressive harmonic generation that softens peaks. **Distortion** is
  the broad family of deliberate nonlinearity. **Clipping** constrains peaks,
  hard or soft.
- Uses beyond "dirty": harmonics for audibility (see sub vs audibility in
  `bass-sub-kick-interaction.md`), lower peak-to-average ratio, transient
  rounding, density, contrast. Saturation before compression can smooth
  difficult transients. Controlled clipping can take drum peaks down while
  holding RMS/LUFS, which buys headroom. [SOS; iZotope, cited in V2 corpus]
- **Saturation for weight instead of EQ boosts** is BOTH (V1 bass playbook
  sources + V1 studies).
- **Which Skill?** A distortion stage *building a patch* is sound design
  (`electronic-production`). Saturation *on a track or bus being balanced*
  is mixing. The mechanism is the same; decide by whether the sound is being
  built or balanced. This boundary is deliberately left as a judgement call
  (LAB design §2).

## Stereo and mono — BOTH

- Width is frequency-dependent. "Width 140%" is not a mix decision. Keep
  critical low-frequency content predictable in mono. [SOURCE-BACKED: V2
  corpus §14, SOS]
- Delay- or phase-based widening can comb-filter, collapse or change level
  when summed to mono. Check mono, Mid only, Side only, and correlation.
  [SOURCE-BACKED]
- **Measured (PROJECT-PROVEN, V1 Study 4):** layering two centred sources
  gave correlation 1.000 (mono), and a detuned unison voice gave 0.400.
  Width comes from deliberate engineering, not from stacking.
- **Measured (PROJECT-PROVEN, V2):** unison-driven mid-bass and pad solos
  measured 0.17 and 0.26 correlation respectively, while the sine sub stayed
  mono by design.

## Space: reverb, delay, sends — SOURCE-BACKED; PARTIAL internally

- Model a space instead of "adding reverb" [V2 corpus §13]: predelay, early
  reflections, tail length, diffusion, damping, frequency-dependent decay,
  width and wet level. Predelay keeps the source transient forward while
  the space trails behind. Not every frequency needs the same reverb, so
  shape the return.
- Delay = time + feedback + filtering + stereo relationship + modulation.
  Synced delays reinforce groove; short unsynced delays double or widen;
  filtered feedback lets repeats recede.
- Use **shared send returns** for sources that belong in one acoustic
  space, and give every reverb or delay one job [V2 corpus §13, §16; RMCP].
- **Internal instances (PARTIAL):** a shared reverb return with its low end
  high-passed (≈300–360 Hz) was used in two V2 pieces to keep the sub out of
  the tail. One is verdict pending; one passed as part of a palette. No
  reverb design has been judged on its own.

## Buses and parallel paths — SOURCE-BACKED

Some processing should act on a **relationship**, not a sound: drum-bus
compression creates interaction, bus saturation gives common colour, a
shared room places unrelated sources in one space, and parallel paths add
character while keeping the original [V2 corpus §16]. Parallel processing
is NOT YET COVERED internally.

## Gain staging and headroom — BOTH

- The principle: don't overload stages unintentionally, and leave headroom
  for later processing. There is **no universal "−18 dBFS" rule**. Measure
  peaks and average level, know when a processor is nonlinear, compensate
  output gain, check buses for accumulation, and level-match before
  judging. [SOURCE-BACKED: V2 corpus §17; iZotope]
- **PROJECT-PROVEN (V2):** a clipping low end was traced to raw sources, not
  processing. Kick, 808 and riser samples measured 65–99% sub-band energy
  each. Fixing their gains at the source cleared the clipping. Measure raw
  sources before blaming the chain.

## Diagnostics — SOURCE-BACKED (V2 corpus §20)

| Symptom | Investigate |
|---|---|
| Muddy | Overlapping low mids, long decays, reverb low end, stacked bass layers |
| Harsh | Resonances, cumulative distortion, too many noise/high layers |
| Flat/static | Not enough modulation, automation or dynamic contrast |
| Small despite many layers | Masking, phase cancellation, no separation of function |
| Overcompressed | Flattened attack, excessive gain reduction, poor release |
| Mono collapses | Phase/time-based widening |
| Reverb mud | Low end in the return, excessive decay, not enough predelay |
| Thin after processing | Phase shift, excessive EQ, cancellation, over-filtering |

## The loop that makes any of this trustworthy

Hypothesis → inspect → least-destructive change → render → compare in
context (not solo) → level-matched A/B → mono check where relevant → keep
or revert → record what worked [V2 corpus §22]. The measurement half is in
`verification-technical-methods.md`; the judgement half is in
`perceptual-judgment-protocol.md`.
