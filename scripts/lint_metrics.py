#!/usr/bin/env python3
"""Objective quality metric for an eval iteration: lint findings per 1000 words.

Usage:
    python scripts/lint_metrics.py <workspace>/iteration-N [--evals evals/evals.json]

Runs skills/writing-docs-in-polish/scripts/lint_pl.py over every Markdown output of
every run, with the register taken from the `register` field of each eval, and prints
a table with_skill vs without_skill. It gives a continuous score (1 error vs 17 errors)
where pass/fail assertions only show FAIL vs FAIL. Also writes lint_metrics.json into
the iteration directory. Stdlib only.
"""
import argparse
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINT_PATH = ROOT / "skills" / "writing-docs-in-polish" / "scripts" / "lint_pl.py"


def load_linter():
    spec = importlib.util.spec_from_file_location("lint_pl", LINT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def measure(lint_pl, run_dir, register):
    words, errors, warnings, codes = 0, 0, 0, Counter()
    for md in sorted((run_dir / "outputs").rglob("*.md")):
        if md.name == "reply.md":
            continue  # the reply is chat, not the document
        words += lint_pl.prose_word_count(md.read_text(encoding="utf-8"))
        for finding in lint_pl.lint(md, register):
            if finding[3] == lint_pl.ERROR:
                errors += 1
            else:
                warnings += 1
            codes[finding[4]] += 1
    return {"words": words, "errors": errors, "warnings": warnings,
            "per_1000": round((errors + warnings) * 1000 / words, 1) if words else None,
            "codes": dict(codes.most_common(5))}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("iteration")
    parser.add_argument("--evals", default=str(ROOT / "evals" / "evals.json"))
    args = parser.parse_args()

    registers = {}
    for path in [Path(args.evals), ROOT / "evals" / "regression-dev-docs.json"]:
        if path.exists():
            for e in json.loads(path.read_text(encoding="utf-8"))["evals"]:
                registers[e["id"]] = e.get("register")

    lint_pl = load_linter()
    iteration = Path(args.iteration)
    table, totals = {}, {"with_skill": Counter(), "old_skill": Counter(), "without_skill": Counter()}
    for eval_dir in sorted(iteration.glob("eval-*")):
        match = re.match(r"eval-(\d+)(?:-|$)", eval_dir.name)
        register = registers.get(int(match.group(1))) if match else None
        if not register:
            print(f"skip {eval_dir.name}: no `register` in evals file", file=sys.stderr)
            continue
        row = {}
        for config in ("with_skill", "old_skill", "without_skill"):
            # layouts seen: <config>/run-1/outputs and <config>/outputs
            runs = sorted((eval_dir / config).glob("run-*")) or ([eval_dir / config] if (eval_dir / config / "outputs").exists() else [])
            if runs:
                row[config] = measure(lint_pl, runs[0], register)
                for key in ("words", "errors", "warnings"):
                    totals[config][key] += row[config][key]
        table[eval_dir.name] = row

    configs = [c for c in ("with_skill", "old_skill", "without_skill") if totals[c]["words"]]
    print(f"{'eval':22}" + "".join(f"{c + ' E/W per1k':>26}" for c in configs))
    for name, row in table.items():
        cells = []
        for config in configs:
            m = row.get(config)
            cells.append(f"{m['errors']:>3}/{m['warnings']:<3} {m['per_1000']:>6}" if m and m["per_1000"] is not None else "-")
        print(f"{name[:22]:22}" + "".join(f"{c:>26}" for c in cells))
    summary = {}
    for config in configs:
        t_ = totals[config]
        summary[config] = round((t_["errors"] + t_["warnings"]) * 1000 / t_["words"], 1)
    print(f"{'TOTAL per 1000 words':22}" + "".join(f"{str(summary[c]):>26}" for c in configs))
    (iteration / "lint_metrics.json").write_text(
        json.dumps({"per_eval": table, "total_per_1000": summary}, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
