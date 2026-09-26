# Repository notes for Claude

This repo ships one Agent Skill: `skills/writing-docs-in-polish/`.

- Follow the Agent Skills spec: `name` in SKILL.md must equal the directory name.
- Keep SKILL.md body under 500 lines; put detail in `references/` (one level deep, linked directly from SKILL.md).
- Skill instructions are in English; examples and templates are in Polish.
- Run `python scripts/validate_skills.py` after editing a skill.
- Keep `version` in sync across SKILL.md `metadata`, `.claude-plugin/plugin.json` and CHANGELOG.md.
- Eval prompts live in `evals/evals.json` (instructional set) and `evals/regression-dev-docs.json` (developer docs); eval workspaces (`*-workspace/`) are gitignored.
