# Provenance, evidence-tier changes and exclusions

This package distils evidence already produced in Bouch audio work. It is
not independently authoritative. If a reference here and its source
disagree, the source wins and this package should be corrected.

## Sources and pins

| Key | Source | Pinned revision | Licence | Role |
|---|---|---|---|---|
| LAB | agent-enumeration-lab: `findings/domain/audio/*` (capability map, portable-vs-REAPER boundary, verification practices, skill boundaries, bouch-audio v0.1 design) | `ea00a04` | own work | Design, boundary and tier synthesis. Consulted, not copied. |
| V1 | reaper-agent-lab (REAPER Agent Lab V1) | tag `v1-evidence-freeze-2026-09-13` = `9df98ef` | own work | Playbooks, studies, sample-ops v1 record, `sample_op.py` + tests |
| V2 | audio-agent-workbench-v2 | `bc460db` (committed state only) | own work; corpus text supplied by the owner, citing public sources | Technique corpus, experiments, `analyze.py` + tests |
| RMCP | reaper-mcp (`github.com/danishaft/reaper-mcp`) | `a5cd892` | MIT (verified: `LICENSE`, `pyproject.toml`) | Mix/master doctrine (canon-attributed) and mastering-safety eval cases |

V1, V2 and LAB were unpublished local repositories when this package was
built, and are referred to by name and revision only. V2 had one
uncommitted working-tree change (a revision of `bass-music-sketch-16bar`,
with verdict PENDING). It was deliberately **not** used: only committed
state was promoted.

## What was promoted, from where

| Package file | Primary sources (read directly) |
|---|---|
| `references/rhythm-groove-drums.md` | V1 `docs/music/playbooks/drums-groove-and-human-feel.md`, V1 `docs/music/studies/first-validation-sprint.md` (Study 2), V2 corpus §6, §8, §18, V2 `docs/experiments/bass-music-sketch-16bar` |
| `references/bass-sub-kick-interaction.md` | V1 `playbooks/bass-and-sub.md`, V1 Study 3, V2 corpus §3, §6, §7, §14, §20, V2 `bass-music-sketch-16bar`, V2 `designed-sound-palette-01` |
| `references/arrangement-and-movement.md` | V1 `playbooks/builds-drops-and-transitions.md`, V1 Study 5, V1 `concrete-bells-v1` (via the playbooks), V2 corpus §15, §19, V2 experiments above |
| `references/sound-design-fundamentals.md` | V2 corpus §1–5, §9, §18, V1 `playbooks/wobble-and-motion.md`, V1 `playbooks/pads-atmosphere-and-space.md`, V1 Studies 1 and 4, V2 `designed-sound-palette-01`, V2 `docs/reconnaissance.md` §8 (class-change heuristic) |
| `references/sample-transformation.md` | V2 corpus §12, V1 `docs/audio-development/sample-ops-slice-v1.md`, V1 `.claude/skills/sample-transform/SKILL.md`, V2 `tools/README.md` |
| `references/mixing-dynamics-and-spatial.md` | V2 corpus §9–11, §13–14, §16–17, §20, §22, RMCP `.agents/skills/reaper-mix-master-engineer/SKILL.md`, V1 Study 4, V2 experiments |
| `references/mastering-boundaries.md` | RMCP Skill (Gates 5–7, decision order, stop conditions), RMCP `evals/mastering-safety-cases.json` + `evals/README.md` |
| `references/verification-technical-methods.md` | V1 `render-and-verify` Skill, V1 sample-ops record, V2 `sidechain-compression-probe`, V2 `designed-sound-palette-01`, V2 `tools/README.md`, RMCP evals |
| `references/perceptual-judgment-protocol.md` | V1 `render-and-verify`, V1 studies' verdict records, V2 blind-audition experiments, RMCP Skill + evals |
| `references/evidence-status.md` | LAB capability map and design §5/§7, re-checked against the sources above |
| `tools/analyze.py`, `tests/test_analyze.py` | V2 `tools/analyze.py`, `tests/test_analyze.py` at `bc460db` (analyze.py matched byte for byte before editing) |
| `tools/sample_op.py`, `tests/test_sample_op.py` | V1 at the freeze tag; sha256 prefixes `c16a3f6e96eefaa2` / `76a8659443a05217` match V1's frozen record exactly |

Changes to the tools on promotion are listed in `tools/README.md`. One of
them changes a measurement. `analyze.py`'s K-weighting filter was
corrected to the BS.1770 reference design. The inherited meter read
0.05–0.09 LU low on real mixes and ~0.25 LU low on a 1 kHz tone, so
absolute loudness figures in V1/V2 records carry that bias (see
`qualification.md`). `sample_op.py`'s checks are unchanged.

## Quote, licence and rights audit (2026-09-18)

- **Third-party text.** The V1 playbooks and V2 corpus contain short verbatim
  quotations from trade press (Sound on Sound, Attack Magazine, MusicRadar)
  and vendor manuals. None was carried over. The references paraphrase the
  technique and cite the article by title/publisher. A grep for each
  source's quoted phrases in `references/` and `skills/` returned nothing.
  The remaining quoted strings are article titles, the two-word technique
  name "EQ bracketing", RMCP eval prompt fragments (MIT) and the
  project owner's own listening verdicts.
- **External URLs** from V1/V2 source lists are not reproduced. Articles
  are cited by title and publisher, and the full links remain in the pinned
  sources.
- **Code.** `analyze.py` and `sample_op.py` are the owner's own work, now
  MIT under this package. `analyze.py` implements the public ITU-R BS.1770-4
  filter and gating definitions.
- **Audio.** No samples, renders or libraries are included. The V1 test
  sample (a MusicRadar royalty-free pack file) and the V2 FM renders are
  referenced only through optional environment variables.
- **RMCP doctrine** is summarised with attribution to the canon it cites
  (Katz, Shepherd, Senior). Those books are credited as the underlying
  authority, and none of their text is reproduced.

## Evidence-tier changes relative to LAB

LAB's capability map was written before V2's latest committed experiments
and was based partly on delegated reads. Checking the sources directly
changed these tiers:

| Claim | LAB tier | Tier here | Why |
|---|---|---|---|
| FM synthesis | NOT YET COVERED | SOURCE-BACKED concept (V2 corpus §2) + **PROJECT-PROVEN, one bounded 2-op voice** | V2 `designed-sound-palette-01` (after LAB's inspection pin `3ab6527`; committed at `bc460db`). Explicitly bounded; general FM stays a gap. |
| Wavetable / granular / additive | NOT YET COVERED | SOURCE-BACKED concept only; still NOT YET COVERED internally | V2 corpus §2 does describe them with manual citations, so "no evidence" was overstated. There is still no internal demonstration. |
| Filters, transient shaping, parallel, reverb | PARTIAL / NOT YET COVERED | SOURCE-BACKED concept + gap (unchanged in substance) | The corpus covers them as concept; the internal gaps are unchanged. |
| Kick/bass arrangement-over-sidechain (V2 sketch) | PROJECT-PROVEN | **Applied, VERDICT PENDING** | The committed V2 record says "Human verdict: PENDING". *Down*-tiered to what the source says. |
| Compression / sidechain avoidance | BOTH | SOURCE-BACKED + applied (VERDICT PENDING) | Same reason. |
| Clean-sub + distorted mid-bass split | SOURCE-BACKED (corpus) | SOURCE-BACKED + PROJECT-PROVEN as a construction | Built in `designed-sound-palette-01`, which passed its human verdict. |
| Movement without automation | PARTIAL (workaround ideas) | PROJECT-PROVEN (two V2 pieces, one passed) | Same experiment. |

No claim was moved upward on the strength of model knowledge or of this
package's own wording.

## Deliberately excluded

- REAPER/MCP operation: V1 `reaper-production` Skill, V2
  `audio-track-assembly`, `reaper-surge-patches` and
  `reaper-decentsampler-instruments` Skills, RMCP tool names, GUID/undo
  semantics and every playbook's "Workbench implementation" section.
  V1 and V2 *disagree* on whether Surge XT's internal FX rack is
  host-controllable (V1: no; V2: yes, for two effect types). That is
  adapter knowledge and was left with the adapters.
- V2 offline tools tied to specific formats or libraries:
  `dx7_voice_extract.py`, `sf2_piano_extract.py`, `sfz_to_dspreset.py`,
  `render_drum_pattern.py`, `reverse_audio.py` (an ffmpeg one-liner whose
  verification lesson is kept in the references). None was needed by the
  consumer test.
- V1 genre maps and `docs/music/contemporary/*`: dated (2024–2026) scene
  vocabulary.
- V1 `docs/audio-development/testing-and-verification.md` acceptance
  harness and onset-detection proposal: PROPOSAL tier, never built.
  Recorded as a gap.
- Single-listener preferences the sources refused to generalise (e.g. V2's
  bass/hook candidate pick; the "Fred again..-adjacent" aesthetic
  reference).
- All render corpora, sample libraries, inventories and project files.
