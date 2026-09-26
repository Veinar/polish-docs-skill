# Evaluating the skill

## Rules

- **Never run the full set.** It has 34 evals and one iteration costs far too many tokens. Run a random sample of about 5 (`scripts/pick_evals.py`). Evals never sampled before are preferred, so the whole set is covered over time.
- **Always use the cheapest model (Haiku).** Runs from different models are not comparable. Record the model with `run_meta.json`.
- **Isolate the baseline.** `without_skill` subagents must not see the skill: run them in an empty scratch directory (or a copy of the repo without `skills/`) and tell them to work only from the task text. Iteration 5 had a baseline that read the skill's templates and quoted its conventions, which made the comparison meaningless.
- **Compare like with like.** Compare versions of the skill on the same evals, on the same model, with the same grading method. Pass rates from different evals or graders are not comparable; lint findings per 1000 words are.
- **Reuse baselines.** `without_skill` runs depend only on the prompt and the model; reuse them and run only `with_skill`.
- **Free metric first.** `scripts/lint_metrics.py` (lint findings per 1000 words) needs no model calls. Grade with assertions only the sampled evals, and only for judgment (completeness, fidelity, naturalness).
- **Watch the cost of a run.** A small task should not cost much more with the skill than without it. If it does, shrink the skill (fast path, on-demand references) before adding rules.

## Files

| File | Purpose |
|---|---|
| `evals/evals.json` | 34 evals (ids 6–39), each with `register` and `tags` |
| `evals/regression-dev-docs.json` | Developer-docs regression set (evals 1–5), run before a release |
| `evals/fixtures/ts-cli/` | Small repository used by eval 37 (camelCase, kebab-case docs, glossary) |
| `scripts/pick_evals.py` | Seeded random sample; prefers evals with fewer earlier runs, spreads tags |
| `scripts/reuse_baselines.py` | `mark` an iteration with its model; `reuse` baselines between iterations |
| `scripts/lint_metrics.py` | Lint findings per 1000 words, with_skill vs without_skill |

## Procedure

```bash
python scripts/pick_evals.py --n 5            # prints ids and the seed
python scripts/pick_evals.py --n 5 --pin 14   # force one in (e.g. an eval you just changed)
python scripts/pick_evals.py --n 4 --tag fidelity
```

```
/skill-creator:skill-creator Run iteration-N of evals/evals.json for skills/writing-docs-in-polish,
ONLY evals with ids <ids>. Use model haiku for every subagent. Run with_skill and without_skill.
Grade only these evals. Generate a static review page.
Every without_skill subagent works in an empty scratch directory and must not read anything under /app/skills or /app/evals; every with_skill subagent may read only the skill directory.
Record total_tokens and duration in timing.json for every run.
```

```bash
python scripts/reuse_baselines.py mark  skills/writing-docs-in-polish-workspace/iteration-N haiku
python scripts/lint_metrics.py          skills/writing-docs-in-polish-workspace/iteration-N
```

When baselines for a sampled eval already exist on the same model, copy them instead of re-running:

```bash
python scripts/reuse_baselines.py reuse skills/writing-docs-in-polish-workspace/iteration-N \
    skills/writing-docs-in-polish-workspace/iteration-M haiku
```

## Before a release

Run the regression set once (`evals/regression-dev-docs.json`) and compare lint findings per 1000 words with the previous release.
