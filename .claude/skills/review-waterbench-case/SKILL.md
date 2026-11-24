---
name: review-waterbench-case
description: Review a WaterBench case repository against the canonical structure spec at STRUCTURE.md. Produces a markdown findings report covering directory layout, controlled vocabulary, README conventions, the observation contract (for model-based cases) — `.dfs0` observation data, a variable-agnostic `stations.csv` manifest with explicit CRS, and manifest↔data referential integrity — and model-setup runnability, i.e. whether the model file references inputs at paths that actually exist in the repo. Read-only — does not modify, push, or open issues.
license: CC BY-NC 4.0
allowed-tools: shell
---

# review-waterbench-case

This is a thin mirror for Claude Code's `.claude/skills/` discovery. The skill itself lives at
[`.github/skills/review-waterbench-case/`](../../../.github/skills/review-waterbench-case/SKILL.md)
— read that SKILL.md and follow its procedure. In short, the checker is:

```
python3 .github/skills/review-waterbench-case/review_case.py --repo <path-to-case-folder>
```

(`python` on Windows.) Its stdout is the complete findings report — relay it, do not add findings
of your own. Run it on a **complete** case folder (large output files present), not a bare clone.
