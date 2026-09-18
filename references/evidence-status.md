# Evidence status: tiers, sources and known gaps

Read this before treating anything in `references/` as settled. Every
substantive claim in the other reference files carries one of the tags
below. Tags were copied from the source that established the claim and are
not upgraded here. Where this package changed a tier, the change and its
reason are recorded in `evidence/PROVENANCE.md`.

## Tier key

| Tag | Meaning | How to use it |
|---|---|---|
| **PROJECT-PROVEN** | Demonstrated inside one of the Bouch audio experiments, with a measurement and/or a recorded human listening verdict. | A reliable starting point. It is still bounded to the material, context and listener it was proven on. |
| **SOURCE-BACKED** | Cited to a named external authority (trade press, manual, textbook). Not re-demonstrated internally. | A reasoned hypothesis to test by rendering and listening. Do not report it as verified. |
| **BOTH** | Source-backed and independently project-proven. | The strongest tier here. |
| **PARTIAL** | Thin: a single instance, or only part of the claim is evidenced. | Usable, but say how thin it is. |
| **OPEN / DISAGREEMENT** | Named sources disagree, or evidence points both ways. | Keep both sides. Choose musically for the task at hand, and don't average them. |
| **HYPOTHESIS** | Plausible and untested. | Something to try, never something to assume. |
| **HUMAN PREFERENCE (single instance)** | One listener preferred one option in one context. | Evidence for that outcome only. Never a rule. |
| **VERDICT PENDING** | The work was done and technically verified, but the source records no human verdict. | The technique was *applied*. Its musical success is unknown. |
| **NOT YET COVERED** | No internal evidence exists. | A gap. Do not fill it from general model knowledge and present the result as package guidance. |

## Source keys

Claims cite short keys. Full pins, licences and what was taken from each
source are in `evidence/PROVENANCE.md`.

- **V1**: REAPER Agent Lab, frozen at tag `v1-evidence-freeze-2026-09-13`.
  Playbooks, studies, `sample_op.py`, `analyze.py`.
- **V2**: Audio Agent Workbench V2 at commit `bc460db`. Experiments,
  `analyze.py`, and the electronic-production technique corpus
  ("V2 corpus §N").
- **RMCP**: reaper-mcp (MIT) at `a5cd892`. The mix/master Skill's
  canon-attributed doctrine and its deterministic mastering-safety evals.
- **LAB**: agent-enumeration-lab audio findings at `ea00a04`. The
  cross-source synthesis that produced this package's design.

## Cross-source strength, in one line each

- Strongest of all: *metrics diagnose, controlled listening approves*.
  Three sources arrived at it independently, and RMCP enforces it with an
  eval (BOTH).
- Strongest production result: structured, role-dependent drum
  humanisation. V1 proved it twice, independently (BOTH).
- Strongest mix result: sub simplicity/mono, with weight coming from
  frequency and arrangement discipline rather than loudness (BOTH).
- Most of the V2 corpus is SOURCE-BACKED only. Roughly two thirds of its
  sections were never exercised in an experiment.

## Bounded project proofs (do not generalise)

- **FM synthesis: one bounded case.** V2 `designed-sound-palette-01` built
  one 2-operator FM bell from init (carrier ratio 1.0, modulator ratio
  ≈3.35, fast modulator envelope). The first algorithm/routing assumption
  was falsified by an A/B render and then corrected. A 21 ms attack-window
  measurement confirmed the FM signature, and the whole palette passed a
  human verdict. That proves one practical FM voice and one verification
  method. It does **not** prove FM synthesis knowledge in general: ratio
  families, index/feedback behaviour, multi-operator design and FM basses
  are SOURCE-BACKED at most (V2 corpus §2).
- **Additive vs subtractive builds.** Both work (PROJECT-PROVEN). Which one
  arrives harder depends on the material (V1 Study 5).
- **Unison/detune vs layering for a pad.** One listener preferred unison for
  one warm target sound (HUMAN PREFERENCE). The rule that did generalise is
  narrower: layering alone measured perfectly mono (PROJECT-PROVEN).
- **Slice-and-rearrange beat untransformed beds.** True for one source, one
  context and one listener (V1 sample-ops v1, provisional).

## Known gaps: NOT YET COVERED internally

None of these has an internal demonstration. Where the V2 corpus says
something about a topic, that material is SOURCE-BACKED concept only. It is
tagged that way where it appears, and it must not be extended from memory.

| Area | What exists | What is missing |
|---|---|---|
| FM beyond the bounded case | Corpus §2 concepts (SOURCE-BACKED); one 2-op bell (PROJECT-PROVEN, bounded) | Multi-operator design, ratio families, feedback, FM bass. |
| Wavetable synthesis | Corpus §2 concept (SOURCE-BACKED) | Any internal demonstration. |
| Granular synthesis/processing | Corpus §2, §12 concept (SOURCE-BACKED) | Any internal demonstration. |
| Additive synthesis | Corpus §2 concept (SOURCE-BACKED) | Any internal demonstration. |
| Filter design | Corpus §5 vocabulary (SOURCE-BACKED); filter-LFO wobble (BOTH) | Filter types and resonance behaviour, demonstrated. |
| Transient shaping | Corpus §8, §10 mentions (SOURCE-BACKED) | Any measured before/after. |
| Leads / plucks | One FM bell-pluck inside a palette (bounded) | Voice-type design knowledge. |
| Per-instrument drum sound design | Only timing/velocity treatment is proven | What makes a kick, clap or hat sonically good. |
| Parallel processing | Corpus §10, §16 (SOURCE-BACKED); one send/return bus used (PARTIAL) | A parallel-compression or parallel-chain demonstration. |
| Reverb design | Corpus §13 parameter model (SOURCE-BACKED); a high-passed reverb return used twice (PARTIAL) | A demonstrated spatial design judged by listening. |
| EQ decisions | Static vs dynamic EQ, location+symptom rule (SOURCE-BACKED) | A measured before/after judged by listening. |
| Automation-driven movement | Corpus §15 (SOURCE-BACKED); movement *without* automation (PROJECT-PROVEN) | Automation-based movement judged by listening. The V2 render path dropped automation, so it was never tested. |
| Sidechain compression pumping | Arrangement-based ducking avoidance was applied (VERDICT PENDING) | An audible sidechain-compression result. It was never achieved end to end. |
| Onset/timing verification | V1 proposal only (never built) | An onset-vs-intended-event checker with a calibrated tolerance. |
| Mastering in practice | RMCP doctrine and safety evals (SOURCE-BACKED + eval-enforced behaviour) | A mastered result judged by listening in any Bouch experiment. |

## Deliberately excluded (not gaps)

- **REAPER, MCP and plugin operation**: tool names, GUID/undo semantics,
  project-state loading, Surge/Dexed/DecentSampler/RS5K mechanics, render
  scripts. These belong to a DAW adapter, not this package.
- **Dated scene and genre vocabulary**: V1 `docs/music/contemporary/` and the
  genre maps (2024–2026 UK club context). It is time-decaying, and it is
  kept out of the timeless core.
- **Libraries, renders and inventories**: sample files, render corpora,
  plugin palettes, machine paths.
- **Single-listener preferences** that the sources themselves refused to
  generalise.
