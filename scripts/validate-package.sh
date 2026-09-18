#!/usr/bin/env bash
# Mechanical package-qualification checks for bouch-audio. Run on every edit.
# Modelled on bouch-agent-core's scripts/validate-package.sh, plus audio-pack
# checks: link traversal, no local paths, no REAPER-operational dependency,
# evidence tags present, and the promoted tools' tests.
# It does not run the activation evals (claude plugin eval; they cost model
# calls) or a consumer test. See evidence/qualification.md for those.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Same agentskills/agentskills pin bouch-agent-core qualifies against.
AGENTSKILLS_REF="69ef37e9424c0a7ea9dd2293b559e43ec8176379"
AGENT_PLUGINS_SCHEMA_URL="https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
LOG_DIR="$(mktemp -d "${TMPDIR:-/tmp}/bouch-audio-validate.XXXXXX")"

FAILED=0
fail() { echo "  ✘ $1"; FAILED=1; }
pass() { echo "  ✔ $1"; }

for tool in claude uvx uv python3; do
  command -v "$tool" >/dev/null 2>&1 || { echo "Required tool not found on PATH: $tool"; exit 2; }
done

echo "== Agent Plugins root schema =="
if uvx check-jsonschema --schemafile "$AGENT_PLUGINS_SCHEMA_URL" plugin.json >"$LOG_DIR/agent-plugins.log" 2>&1; then
  pass "plugin.json conforms to Agent Plugins v1.0.0"
else
  fail "plugin.json does not conform (see $LOG_DIR/agent-plugins.log)"
fi

echo "== Agent Skills validation =="
for skill_dir in skills/*/; do
  name="$(basename "$skill_dir")"
  if uvx --from "git+https://github.com/agentskills/agentskills.git@${AGENTSKILLS_REF}#subdirectory=skills-ref" \
      skills-ref validate "$skill_dir" >"$LOG_DIR/skill.$name.log" 2>&1; then
    pass "skills/$name"
  else
    fail "skills/$name (see $LOG_DIR/skill.$name.log)"
  fi
done

echo "== Claude plugin --strict =="
if claude plugin validate "$REPO_ROOT" --strict >"$LOG_DIR/claude.log" 2>&1; then
  pass "claude plugin validate --strict"
else
  fail "claude plugin validate --strict (see $LOG_DIR/claude.log)"
fi

echo "== Portable <-> Claude identity consistency =="
if python3 - <<'PYEOF'
import json, sys
root = json.load(open("plugin.json"))
claude = json.load(open(".claude-plugin/plugin.json"))
bad = [f for f in ("name", "version", "description", "author", "keywords") if root.get(f) != claude.get(f)]
sys.exit(1 if bad else 0)
PYEOF
then pass "identity fields identical"; else fail "identity fields diverged"; fi

echo "== Structure =="
[ -e .codex-plugin ] && fail ".codex-plugin/ present (not needed)" || pass "no .codex-plugin/"
[ -e SKILL.md ] && fail "root SKILL.md present (no router by design)" || pass "no root SKILL.md router"
stray=$(find . -path ./.git -prune -o \( -iname plugin.json -o -iname marketplace.json \) -print \
  | grep -vE '^\./(plugin\.json|\.claude-plugin/plugin\.json)$')
[ -n "$stray" ] && fail "stray manifests: $stray" || pass "no stray manifests"

echo "== Reference traversal (every relative Markdown link resolves) =="
if python3 - <<'PYEOF'
import os, re, sys
bad, n = [], 0
for base in ("skills", "references", "tools", "evidence", "README.md"):
    paths = [base] if base.endswith(".md") else [os.path.join(d, f) for d, _, fs in os.walk(base) for f in fs if f.endswith(".md")]
    for p in paths:
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", open(p).read()):
            if "://" in target:
                continue
            n += 1
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), target))):
                bad.append(f"{p} -> {target}")
# Every reference file is reachable from at least one Skill.
linked = set()
for d, _, fs in os.walk("skills"):
    for f in fs:
        for t in re.findall(r"\]\((\.\./\.\./references/[^)#\s]+)", open(os.path.join(d, f)).read()):
            linked.add(os.path.basename(t))
orphans = sorted(set(os.listdir("references")) - linked)
for b in bad: print("   broken:", b)
for o in orphans: print("   not reachable from any Skill:", o)
print(f"   {n} relative links checked")
sys.exit(1 if bad or orphans else 0)
PYEOF
then pass "all relative links resolve; every reference reachable from a Skill"; else fail "reference traversal"; fi

echo "== No absolute or machine-local paths =="
# Tracked files only: gitignored local output (eval results) legitimately
# records the checkout path and is never published.
hits=$(git ls-files -z -- skills references tools tests evidence evals evals-control README.md plugin.json .claude-plugin \
  | xargs -0 grep -nE '/home/|/Users/|/usr/bin/python|~/\.|[A-Z]:\\\\' 2>/dev/null || true)
[ -n "$hits" ] && { echo "$hits" | sed 's/^/   /'; fail "local paths found"; } || pass "no local paths"

echo "== No REAPER-operational dependency in Skills/references/tools =="
# Tool-surface vocabulary from the excluded adapters, matched case-sensitively.
# The "Deliberately excluded" section of evidence-status.md names these on
# purpose and is skipped; nothing else may mention them.
if python3 - <<'PYEOF'
import os, re, sys
ops = re.compile(r"reaper-mcp-cli|set_fx_parameter|render_project|insert_audio_item|load_fx_|ensure_track_envelope|list_available_fx|\bGUID|undo step|\.RPP\b|\bRS5K\b|ReaComp|ReaEQ|ReaLimit|ReaVerbate|\bJSFX\b|vst_chunk|dspreset|\bMCP\b")
hits = []
for base in ("skills", "references", "tools"):
    for d, _, fs in os.walk(base):
        for f in fs:
            if not f.endswith((".md", ".py")):
                continue
            p = os.path.join(d, f)
            text = open(p).read()
            if p == os.path.join("references", "evidence-status.md"):
                text = text.split("## Deliberately excluded")[0]
            for i, line in enumerate(text.splitlines(), 1):
                if ops.search(line):
                    hits.append(f"{p}:{i}: {line.strip()}")
for h in hits: print("  ", h)
sys.exit(1 if hits else 0)
PYEOF
then pass "no REAPER/MCP operational terms"; else fail "REAPER/MCP operational terms found"; fi

echo "== Evidence tags present =="
if python3 - <<'PYEOF'
import os, re, sys
tags = re.compile(r"PROJECT-PROVEN|SOURCE-BACKED|\bBOTH\b|PARTIAL|OPEN / DISAGREEMENT|HYPOTHESIS|VERDICT PENDING|NOT YET COVERED|HUMAN PREFERENCE")
missing = [f for f in os.listdir("references") if not tags.search(open(os.path.join("references", f)).read())]
for f in sorted(os.listdir("references")):
    print(f"   {f}: {len(tags.findall(open(os.path.join('references', f)).read()))} tier tags")
sys.exit(1 if missing else 0)
PYEOF
then pass "every reference carries tier tags"; else fail "reference without tier tags"; fi
grep -q "NOT YET COVERED" references/evidence-status.md && pass "gap list present in evidence-status.md" || fail "gap list missing"

echo "== Promoted tool tests (fresh environment, current numpy/scipy) =="
if uv run --no-project --with numpy --with scipy --with pytest python -m pytest -q -W error::DeprecationWarning tests/ >"$LOG_DIR/pytest.log" 2>&1; then
  pass "$(tail -1 "$LOG_DIR/pytest.log")"
else
  tail -20 "$LOG_DIR/pytest.log" | sed 's/^/   /'; fail "tool tests"
fi

echo
[ "$FAILED" -eq 0 ] && echo "validate-package: ALL CHECKS PASSED" || echo "validate-package: FAILED (logs in $LOG_DIR)"
exit "$FAILED"
