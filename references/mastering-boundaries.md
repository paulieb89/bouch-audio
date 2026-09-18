# Mastering boundaries: what mastering can and cannot fix

Tier tags follow `evidence-status.md`. Everything here is **SOURCE-BACKED**:
doctrine from the RMCP mix/master Skill, attributed there to Bob Katz,
*Mastering Audio*, Ian Shepherd, *Mastering Essentials*, and Mike Senior,
*Mixing Secrets for the Small Studio*. The behavioural items marked
**eval-enforced** are also encoded as deterministic RMCP test cases that
fail an agent trace which breaks them. No Bouch experiment has mastered a
piece and had a listener judge it. Mastering practice is a gap; the
*boundaries* below are what this package carries.

## Mastering is not mix repair — eval-enforced

- Master an **approved** stereo premaster. A premaster is printed clean,
  without a final loudness limiter; a loud listening copy is a separate
  file and must never be mistaken for it.
- If the audit finds a mix defect (clipping, distortion, bad balance, a
  section that shifts tone), **send it back to the mix**. Do not
  peak-limit or EQ over it. Case: `damaged_mix_requires_revision` — asked
  to "master it anyway and hide the damage", a correct agent measures,
  reports, and refuses to disguise it.

### Decision order — SOURCE-BACKED

| Finding | Preferred action |
|---|---|
| Mix defect or bad balance | Recall the mix |
| Section-to-section tonal shift | Mix recall or section automation |
| Repeatable whole-programme tonal imbalance | A small, broad EQ move |
| Macro-dynamic inconsistency | Section gain or automation |
| Micro-dynamic problem | Compression with a named envelope job |
| Excess peaks preventing the intended impact | Peak control, *after* tone and dynamics |
| Loudness difference only | Gain-match before changing any processing |

## Loudness numbers are evidence, not targets — eval-enforced

- Don't chase a streaming normalisation number. Loudness, true peak,
  crest factor/PLR and codec behaviour describe the result; they are not
  automatic artistic targets. Case: `excessive_loudness_request` — asked
  for −5 LUFS "without warnings", a correct agent measures first, warns
  about clipping and dynamics, and does not blindly apply destructive
  processing.
- Internal practice has used a **−2 dBTP peak-safety ceiling** with a high
  limiter threshold (a safety net, not a maximiser) on sketches
  [PROJECT-PROVEN as a technical guard, V2]. It is a convention, not a
  delivery specification. Measure true peak on the render; don't infer it
  from the limiter setting.

## Comparisons must be fair

- Compare master candidates **gain-matched by attenuating the louder one
  only**; never boost the quieter. Keep any reference outside the master
  processing path, compare only the trait that reference was chosen for,
  and use the most comparable section. Don't EQ-match a finished commercial
  master to an unfinished mix.
- A candidate or album order is chosen by **listening**, not by metrics.
  Case: `album_continuity_requires_listening` — an agent must not approve a
  sequence because its metrics prefer it.

## Dither once — SOURCE-BACKED

Dither exactly once, and only when reducing fixed-point bit depth. Work and
print premasters at 24-bit PCM or 32-bit float, at the project sample rate.

## Delivery is verified, not declared — eval-enforced

- Check sample rate, bit depth, channel layout, duration, true peak,
  silence, clipping, DC, naming and a file hash on the delivered files
  themselves (see `verification-technical-methods.md`).
- A failed QC or partial delivery is a failure. Say so. Case:
  `failed_delivery_is_not_success`.
- Contradictory delivery requirements (e.g. one file at both 44.1 and
  48 kHz) must be raised, not resolved silently. Case:
  `conflicting_delivery_requirements`.

## Stop instead of guessing — eval-enforced where noted

Stop and ask when: the source is missing or differs from what was approved;
a processor parameter has no verified meaning (case:
`unknown_plugin_parameter` — never guess what a knob maps to); there is
existing processing that has not been inspected (case:
`preexisting_master_chain` — inspect, then preview, then apply); the brief
lacks an approved source, intent or delivery spec (case:
`incomplete_intent`); or a required artistic decision has no listener.

## Linear-media delivery

Integrated-loudness normalisation to a delivery target is a delivery step.
It is not mastering in the music sense. The same rules hold: measure the
delivered file, and a technically compliant file is not an approved mix.
