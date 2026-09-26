# Repository notes for Claude

This repo ships one Agent Skill: `skills/writing-docs-in-polish/`.

- Follow the Agent Skills spec: `name` in SKILL.md must equal the directory name.
- Keep SKILL.md body under 500 lines; put detail in `references/` (one level deep, linked directly from SKILL.md).
- Token budget: SKILL.md is loaded on every use (validator limit about 2.5 k tokens). Put anything not needed every time into `references/`, keep lookups in `scripts/term.py`, and never let the workflow read whole glossaries.
- Skill instructions are in English; examples and templates are in Polish.
- Dashes: en dash (U+2013) only, never the em dash (U+2014), in every file of this repo. `validate_skills.py` fails on it.
- The repository language for Polish documents is decided by `scripts/detect_conventions.py`; match a project's naming case, do not force snake_case.
- After editing a skill run `python scripts/validate_skills.py`, `python -m unittest discover -s scripts` and `python skills/writing-docs-in-polish/scripts/lint_pl.py --strict --ignore placeholder-prose skills/writing-docs-in-polish/assets/templates`.
- Keep the version in sync across `VERSION`, SKILL.md `metadata`, `.claude-plugin/plugin.json` and the latest release in CHANGELOG.md (checked by `validate_skills.py`).
- Never run the full eval set: sample with `scripts/pick_evals.py`, use the cheapest model (Haiku), see `evals/README.md`.
- Eval prompts live in `evals/evals.json` (instructional set) and `evals/regression-dev-docs.json` (developer docs); eval workspaces (`*-workspace/`) are gitignored.
