# Repository notes for Claude

This repo ships one Agent Skill: `skills/writing-docs-in-polish/`.

- Follow the Agent Skills spec: `name` in SKILL.md must equal the directory name.
- Token budget: SKILL.md is loaded on every use (validator limit about 2.5 k tokens). Put anything not needed every time into `references/`, keep lookups in `scripts/term.py`, and never let the workflow read whole glossaries.
- Keep SKILL.md body under 500 lines; put detail in `references/` (one level deep).
- Skill instructions are in English; examples and templates are in Polish.
- After editing a skill run `python scripts/validate_skills.py`, `python -m unittest discover -s scripts` and `python skills/writing-docs-in-polish/scripts/lint_pl.py --strict --ignore placeholder-prose,template-comment skills/writing-docs-in-polish/assets/templates`.
- Keep the version in sync across `VERSION`, SKILL.md `metadata`, `.claude-plugin/plugin.json` and the latest release in CHANGELOG.md (checked by `validate_skills.py`).
- Evals: never run the full set; sample with `scripts/pick_evals.py` on the cheapest model, see `evals/README.md`.
- Keep this file free of rules about how Polish documents are written: evaluation subagents read it, and it would leak into the baseline. Those rules belong in SKILL.md.
