---
name: mixing-and-mastering
description: Evidence-tagged reasoning for balancing, diagnosing and finishing audio that already exists — mix problems (muddy, harsh, flat, small, masked kick, weak sub, clipping master), EQ vs dynamic EQ, compression jobs, saturation on tracks/buses, sidechain and ducking decisions, stereo width and mono compatibility, reverb/delay sends, gain staging, and what mastering can and cannot fix (loudness targets, true peak, dither, delivery). Use when a mix or soundtrack needs diagnosing or improving, before or during mastering, when choosing between processing options, or when asked to hit a loudness number. Not for designing new sounds or arrangements (use electronic-production), and not for measuring or verifying a render (use audio-verification).
metadata:
  package: bouch-audio
  evidence: tiered; see references/evidence-status.md
---

# Mixing and mastering

Most of this area is SOURCE-BACKED doctrine that has not been
re-demonstrated in Bouch experiments. Treat each move as a hypothesis:
change one thing, render, level-match, and let a listener decide.

## Working order

1. **Name the problem and its evidence.** Where does it occur and what
   shows it exists: a measurement, or a listener's report? No named
   problem, no processor.
2. **Try the earlier fix first.** Arrangement, source choice, level, pan,
   timing. The static balance with no processing is the control condition
   for every later comparison.
3. **Smallest reversible change**, with a stated job (e.g. "compress to
   even phrase level", never "drums need compression").
4. **Render, compare in context, loudness-matched**, check mono where it
   matters, then keep or revert. Record what worked.
5. **Mastering starts from an approved mix.** A mix defect goes back to
   the mix. Loudness figures are evidence, not targets.

## Route to the reference

| Decision | Read |
|---|---|
| EQ, compression, saturation, stereo/mono, reverb/delay/sends, buses, gain staging, symptom diagnostics | [`../../references/mixing-dynamics-and-spatial.md`](../../references/mixing-dynamics-and-spatial.md) |
| Kick vs bass conflicts, sidechain vs arrangement, sub mono, low-end clipping | [`../../references/bass-sub-kick-interaction.md`](../../references/bass-sub-kick-interaction.md) |
| Premaster, mastering decision order, loudness requests, true peak, dither, delivery, stop conditions | [`../../references/mastering-boundaries.md`](../../references/mastering-boundaries.md) |
| Which claims are proven, source-backed, or gaps | [`../../references/evidence-status.md`](../../references/evidence-status.md) |

## Hard rules (eval-enforced in the source doctrine)

- Never disguise a mix defect with mastering processing. Recall the mix.
- Never apply destructive processing to hit a requested LUFS figure
  without measuring first and stating the cost.
- Never guess what an unknown processor parameter does. Inspect it first.
- Inspect existing processing before adding to it.
- A failed or partial delivery is a failure. Report it as one.
- You cannot hear. Never claim a listening judgement; route it to a
  human (`audio-verification`).

## Boundaries with the other Skills

- Designing or rebuilding a sound or section: `electronic-production`.
  Saturation *inside a patch* is sound design; *on a track or bus* it is
  mixing.
- Measuring renders, fair A/B preparation and verdict recording:
  `audio-verification`.

## Deliberately not here

DAW-specific operation, plugin preset chains, and "copy the reference's
EQ curve". Known gaps (no internal EQ before/after, no demonstrated reverb
design or parallel processing, no listener-judged master) are listed in
`evidence-status.md`. Don't paper over them.
