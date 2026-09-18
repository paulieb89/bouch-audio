# Qualification record: bouch-audio v0.1.0 (experimental baseline)

Date: 2026-09-18. Claude Code 2.1.276. Tools tested under numpy 1.26.4 /
scipy 1.16.3 and numpy 2.5.3 / scipy 1.18.1 (Python 3.12).

Status: **qualified experimental baseline**. Packaging, activation,
traversal and one real consumer task pass. Musical quality of the consumer
output is **VERDICT PENDING** (human listening), as it must be.

## 1. Mechanical package checks: `scripts/validate-package.sh`

All pass:

- Agent Plugins v1.0.0 schema (`plugin.json`, via `check-jsonschema`)
- Agent Skills `skills-ref validate` for all three Skills, at
  agentskills@`69ef37e9`
- `claude plugin validate --strict`
- identity fields identical between `plugin.json` and
  `.claude-plugin/plugin.json`
- no `.codex-plugin/`, no root `SKILL.md` router, no stray manifests
- reference traversal: all relative links resolve, and every reference
  file is reachable from at least one Skill
- no absolute or machine-local paths
- no REAPER/MCP operational vocabulary in Skills, references or tools
- every reference carries evidence-tier tags, and the gap list is present
- tool tests: 39 passed, 2 skipped (optional real-material checks, run
  separately below)

**Positive control (the checks can fail).** A scratch copy seeded with one
fault per check (a local path, a REAPER tool name, a broken link, an
invalid Skill name, a diverged manifest version, a root `SKILL.md`, an
untagged unreachable reference, and two `analyze.py` mutations) failed
every targeted check. The agentskills validator named the bad Skill, and
the test suite caught both analyzer mutations once the known-positive tests
below were added.

## 2. Promoted tools

| Tool | Result |
|---|---|
| `analyze.py` + `tests/test_analyze.py` | 15 tests + 1 optional. The optional test was run against the original V2 FM renders (`ANALYZE_BELL_RENDERS`) and passed. |
| `sample_op.py` + `tests/test_sample_op.py` | 24 tests + 1 optional. The optional test was run against the original V1 real-material sample (`SAMPLE_OP_REAL_MATERIAL`) and passed. |

Both suites pass on both numpy/scipy stacks, including with
`-W error::DeprecationWarning` on numpy 2.x.

**Defect found and fixed during promotion.** The inherited suite did not
fail when the clip detector was broken (a mutation run). Known-positive
tests were added for the EBU 1 kHz −23 dBFS reference, clipping,
inter-sample true peak, silence runs and mono cancellation. The reference
test then exposed a real measurement defect: the inherited K-weighting
design read −23.25 LUFS against ffmpeg `ebur128`'s −23.0. The filter was
redesigned to the BS.1770 reference; coefficient error against the
published 48 kHz values is now < 1e-15. Cross-check on eight real
V1/V2 renders (integrated LUFS):

| Render | Inherited | Corrected | ffmpeg ebur128 |
|---|---|---|---|
| 8bar-house-arrangement-01 | −18.96 | −18.88 | −18.9 |
| audition-doomsday | −16.45 | −16.38 | −16.4 |
| audition-icebreaker-hook | −12.57 | −12.52 | −12.5 |
| bass-music-sketch-16bar | −11.22 | −11.13 | −11.1 |
| designed-sound-palette-01 | −14.28 | −14.23 | −14.2 |
| sidechain-compression-probe | −11.82 | −11.77 | −11.8 |
| studio-core-sprint | −17.34 | −17.25 | −17.3 |
| uk-club-8bar-experiment-01 | −12.54 | −12.49 | −12.5 |

The same defect exists in the V1 and V2 source copies. V1 is frozen and
stays unchanged by decision (2026-09-18), so loudness figures in its
records carry the small low bias noted above. V2 has not been changed.

## 3. Skill activation, non-activation and traversal: `claude plugin eval`

`claude plugin eval . --ablation none --runs 3 --concurrency 4`, with 10
cases × 3 runs = 30 runs. **Every run of every case scored 1.0** (cost
$6.04). Graders are deterministic `tool_used`/`regex` checks only; there is
no LLM judge.

| Case | Checks |
|---|---|
| pos-sub-bass-rebuild | `electronic-production` fires; reads `bass-sub-kick-interaction.md`; answer names sine/triangle |
| pos-robotic-drums | `electronic-production` fires; reads `rhythm-groove-drums.md`; answer ties tightness/lay-back to roles |
| pos-muddy-mix-sidechain | `mixing-and-mastering` fires; answer puts arrangement/spectral/decay options before a reflexive sidechain |
| pos-loudness-request | `mixing-and-mastering` fires; answer raises the mix/clipping problem |
| pos-render-check-and-ab | `audio-verification` fires; reads a verification reference; answer refuses to claim it heard anything |
| pos-fm-transient-verify | a production or verification Skill fires; answer points at windowed/attack analysis |
| gap-granular-honesty | `electronic-production` fires; reads the evidence status; answer states that granular is **not** internally proven, instead of inventing a recipe |
| neg-csv-parsing | no bouch-audio Skill fires |
| neg-pipewire-device (near-miss: audio word, systems task) | no bouch-audio Skill fires |
| neg-colour-grade (near-miss: linear-media, picture task) | no bouch-audio Skill fires |

**Negative-grader control.** The `min: 0, max: 0` grader was run against an
audio prompt (`evals-control/`, 2 runs). It scored 0 both times. The
non-activation passes above therefore come from a working instrument.

Limits: the with/without-plugin ablation was not run (`--ablation none`),
so this measures activation and routing, not answer uplift against a
baseline. The judge-free graders check routing and key content, not
answer quality.

## 4. Real consumer acceptance: Linear Media sound-to-picture

**Consumer.** A clean clone of linear-media-agent-lab at `73efd60`, whose
`sound-to-picture` Skill reached audio knowledge through sibling-repository
paths (`reaper-agent-lab/docs/...`, `audio-agent-workbench-v2/docs/...`).
One consumer-side edit rewired its routing table to the three bouch-audio
Skills (`consumer-linear-media-skill-routing.diff`). The package was loaded
from a clean clone at `6048d55` with `--plugin-dir`, in a headless
`claude -p` session.

**Task.** A real open item from that project: ARC ONE's interaction sounds
(detent ticks at 7.35–15.55 s, press-confirm at 21.83 s) were built "with
no domain sound-design cross-reference". The session had to redesign them
for weight on small speakers, verify technically, and prepare a blind A/B,
without touching the rest of the score or picture.

**What happened (from the session trace; 62 turns, $3.56).**

- Skills invoked: `sound-to-picture` → `bouch-audio:electronic-production`
  → `bouch-audio:audio-verification`.
- Package files read by relative path: `bass-sub-kick-interaction.md`,
  `evidence-status.md`, `perceptual-judgment-protocol.md`,
  `sound-design-fundamentals.md`, `tools/README.md`. Package tool run:
  `tools/analyze.py` (whole-file and windowed).
- Design applied from the references: a function-layered tick
  (weight/body + a harmonic layer for audibility + contact click), and a
  press hit built as pitch transient + clean sub + separately distorted
  octave layer + click. Each technique was tagged with its evidence tier,
  including naming transient shaping as a recorded gap and the
  bass-to-foley transfer as HYPOTHESIS.
- Verification: the legacy render is **byte-identical** to the committed
  score (re-confirmed independently: sha256 `bc8678b4…`). The new score
  differs from the old by ≤ 1 LSB outside the edited windows. No clipping;
  whole-mix loudness moved by 0.06 LU. Windowed measurements show the
  intended spectral change. The session caught and fixed its own first
  press design (11 dB short on sub) by measurement.
- Blind A/B: a 6–24 s excerpt, matched by attenuation only. Independently
  re-measured by ffmpeg `ebur128` at −16.5 LUFS for both, with the answer
  key in a separate file. The session found that ffmpeg `loudnorm`
  disagreed with two other meters by ~0.1 LU and switched to the package
  meter.
- The report says what the measurements do and do not prove, states that
  the agent cannot hear, and leaves the verdict PENDING.

**Falsification checks** (LAB design §12):

| Condition | Result |
|---|---|
| A portable Skill or reference had to be edited to fit the consumer | **No.** The package clone was unmodified after the session (clean `git status`). |
| A REAPER/DAW operation or dependency was needed | **No.** Zero tool calls touched REAPER, MCP or the sibling source repositories. |
| A verification practice failed to generalise to a non-REAPER pipeline | **No.** Postcondition re-derivation, windowed analysis and the loudness-matched blind A/B all applied to a numpy synthesis pipeline unchanged. |

**Not established:** whether the redesign sounds better. The human verdict
on the A/B is pending.

**Preserved, not adopted (2026-09-18).** The A/B, answer key, candidate
patches and measurements are committed in linear-media-agent-lab at
`5339ba5`, under `docs/experiments/bouch-audio-foley-ab/`, as evidence
only. That project's product (`src/`, `audio/`, timeline, Skills, final
render) is unchanged. Applying the candidate patch to `73efd60`
regenerates the A/B files byte for byte.

## 5. Consumer-side follow-up (outside this package)

Linear Media's `references/picture-sync-and-mix.md` still cites V1/V2
paths and corpus section numbers. It worked in this test because the
session routed through bouch-audio first. Retargeting it to bouch-audio
reference names is a Linear Media change, not a package change.
