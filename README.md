# bouch-audio

A portable, evidence-tiered audio domain capability for agents: reasoning
for electronic production, mixing and mastering, and audio verification.
It includes two tested deterministic tools. It does not depend on any DAW.

Registry identity: `dev.bouch/audio`. Status: **experimental** (v0.1.0).

## What this is

- **Three Skills** that carry reusable reasoning and route into references:
  - `electronic-production`: building material that doesn't exist yet
    (sound design, bass/drums, arrangement, movement, resampling).
  - `mixing-and-mastering`: balancing and diagnosing material that exists,
    and what mastering can and cannot fix.
  - `audio-verification`: proving technical properties by measurement, and
    routing perceptual and musical judgement to a human listener.
- **Shared references** (`references/`): detailed knowledge in which every
  claim is tagged PROJECT-PROVEN, SOURCE-BACKED, BOTH, PARTIAL, OPEN,
  HYPOTHESIS, VERDICT PENDING or NOT YET COVERED. Start with
  [`references/evidence-status.md`](references/evidence-status.md).
- **Tools** (`tools/`): `analyze.py` (BS.1770 loudness, true peak,
  clipping, stereo, spectrum, windowed analysis) and `sample_op.py`
  (manifest-verified slice/arrange/reverse/repitch). See
  [`tools/README.md`](tools/README.md).
- **Evidence** (`evidence/`): source pins, the quote and licence audit,
  evidence-tier changes, exclusions and the qualification record.

## What this is not

- Not a DAW adapter. No REAPER, MCP or plugin operation, project state or
  render scripts. A future adapter should route *into* these references,
  not copy them.
- Not a sample library, render corpus or plugin inventory.
- Not a survey of audio production. It covers what Bouch experiments
  actually exercised or sourced; the gaps are listed, not filled.
- Not an authority on taste. Measurement proves technical properties;
  listening decides musical ones.

## Layout

```
bouch-audio/
├── plugin.json                 # Agent Plugins 1.0.0 manifest (canonical identity)
├── .claude-plugin/plugin.json  # Claude adapter manifest (same identity fields)
├── skills/
│   ├── electronic-production/SKILL.md
│   ├── mixing-and-mastering/SKILL.md
│   └── audio-verification/SKILL.md
├── references/                 # shared, linked from Skills by relative path
├── tools/                      # analyze.py, sample_op.py (+ README)
├── tests/                      # pytest suites for the tools
├── evals/                      # claude plugin eval: activation / non-activation / traversal
├── evidence/                   # PROVENANCE.md, qualification.md
└── scripts/validate-package.sh
```

There is no root `SKILL.md`. Skills are discovered at
`skills/<name>/SKILL.md`. The root `references/` directory is a working
pattern shared with bouch-agent-core; it is not a spec-defined location,
and each Skill reaches it through explicit `../../references/…` links.

## Using it

Claude Code, for one session:

```
claude --plugin-dir /path/to/bouch-audio
```

Other Agent Skills clients: point the client at `skills/`, keeping the
repository tree intact so the `../../references` and `../../tools` links
resolve. The tools need Python ≥ 3.10 with numpy and scipy, or `uv run`.

## Qualifying a change

```
scripts/validate-package.sh                                  # manifests, skills, links, paths, tags, tests
claude plugin eval . --ablation none --runs 3 --trust-plugin # activation evals (model cost)
```

The current qualification record is
[`evidence/qualification.md`](evidence/qualification.md).

## Licence

MIT (see `LICENSE`). Third-party techniques are paraphrased and cited by
title and publisher; no third-party text, audio or renders are included.
See [`evidence/PROVENANCE.md`](evidence/PROVENANCE.md).
