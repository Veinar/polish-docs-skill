# Evaluating the skill

## Rules

- **Always run evals on the cheapest model (Haiku).** Runs from different models are not comparable, and a rule that works on Haiku works on larger models. Record the model with `run_meta.json`.
- **Reuse baselines.** The `without_skill` runs depend only on the prompt and the model. Reuse them and re-run only the `with_skill` side.
- **Judge with two metrics.** Pass/fail assertions (judgment: completeness, fidelity, naturalness) and lint findings per 1000 words (mechanical: typography, calques, placeholders). Do not spend grader assertions on what the linter measures.

## Files

| File | Purpose |
|---|---|
| `evals/evals.json` | 34 evals (ids 6–39), each with a `register` and `tags` (run a subset by tag, e.g. `fidelity` or `invented-facts`) |
| `evals/regression-dev-docs.json` | Developer-docs regression set (evals 1–5) |
| `evals/fixtures/ts-cli/` | Small repository used by eval 19 (camelCase, kebab-case docs, glossary) |
| `scripts/reuse_baselines.py` | `mark` an iteration with its model; `reuse` baselines between iterations |
| `scripts/lint_metrics.py` | Lint findings per 1000 words, with_skill vs without_skill |

## Procedure

First iteration on a model (no baselines to reuse yet):

```
/skill-creator:skill-creator Run iteration-N of evals/evals.json for skills/writing-docs-in-polish.
Use model haiku for every subagent. Run with_skill and without_skill. Generate a static review page.
```

```bash
python scripts/reuse_baselines.py mark skills/writing-docs-in-polish-workspace/iteration-N haiku
python scripts/lint_metrics.py skills/writing-docs-in-polish-workspace/iteration-N
```

Later iterations (baselines already exist on the same model):

```bash
python scripts/reuse_baselines.py reuse skills/writing-docs-in-polish-workspace/iteration-N \
    skills/writing-docs-in-polish-workspace/iteration-M haiku
```

```
/skill-creator:skill-creator Run iteration-M of evals/evals.json for skills/writing-docs-in-polish.
Use model haiku. The without_skill runs already exist for the listed evals (re-grade them);
run without_skill only for the evals reported as "run fresh". Generate a static review page.
```

Then `python scripts/lint_metrics.py …/iteration-M`, open `review.html`, and put the downloaded `feedback.json` into the iteration directory.

## Before a release

Run the regression set once (`evals/regression-dev-docs.json`) and compare lint findings per 1000 words with the previous release.
