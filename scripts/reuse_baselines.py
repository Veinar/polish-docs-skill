#!/usr/bin/env python3
"""Reuse baseline (without_skill) runs between eval iterations to halve the cost.

The baseline does not depend on the skill, so it only has to be re-run when an eval
prompt or the model changes.

Usage:
    python scripts/reuse_baselines.py mark  <iteration> <model>
    python scripts/reuse_baselines.py reuse <previous> <new> <model> [--evals evals/evals.json]

`mark` records which model produced an iteration (run_meta.json). `reuse` copies the
without_skill outputs and timings from <previous> into <new> for every eval whose
prompt is unchanged, refusing when the recorded models differ (a baseline from another
model would make the comparison meaningless). Gradings are NOT copied: assertions may
have changed, so re-grade the reused outputs. Stdlib only.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_prompts(evals_path):
    prompts = {}
    for path in [Path(evals_path), ROOT / "evals" / "regression-dev-docs.json"]:
        if path.exists():
            for e in json.loads(path.read_text(encoding="utf-8"))["evals"]:
                prompts[e["id"]] = e["prompt"]
    return prompts


def recorded_model(iteration):
    meta = Path(iteration) / "run_meta.json"
    return json.loads(meta.read_text(encoding="utf-8")).get("model") if meta.exists() else None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    mark = sub.add_parser("mark")
    mark.add_argument("iteration")
    mark.add_argument("model")
    reuse = sub.add_parser("reuse")
    reuse.add_argument("previous")
    reuse.add_argument("new")
    reuse.add_argument("model")
    reuse.add_argument("--evals", default=str(ROOT / "evals" / "evals.json"))
    args = parser.parse_args()

    if args.command == "mark":
        (Path(args.iteration) / "run_meta.json").write_text(json.dumps({"model": args.model}) + "\n", encoding="utf-8")
        print(f"{args.iteration}: model recorded as {args.model}")
        return 0

    previous, new = Path(args.previous), Path(args.new)
    old_model = recorded_model(previous)
    if old_model != args.model:
        print(f"Refusing: {previous} has model {old_model!r}, requested {args.model!r}. "
              f"Run baselines on {args.model} once and `mark` that iteration.", file=sys.stderr)
        return 1
    prompts = load_prompts(args.evals)
    reused, fresh = [], []
    for old_dir in sorted(previous.glob("eval-*")):
        match = re.match(r"eval-(\d+)-", old_dir.name)
        source = old_dir / "without_skill"
        target = new / old_dir.name / "without_skill"
        meta = old_dir / "eval_metadata.json"
        if not (match and source.exists() and meta.exists()):
            continue
        unchanged = prompts.get(int(match.group(1))) == json.loads(meta.read_text(encoding="utf-8")).get("prompt")
        if unchanged and not target.exists():
            shutil.copytree(source, target, ignore=shutil.ignore_patterns("grading.json"))
            reused.append(old_dir.name)
        else:
            fresh.append(old_dir.name)
    (new / "run_meta.json").write_text(json.dumps({"model": args.model}) + "\n", encoding="utf-8")
    print(f"reused baselines ({len(reused)}): {', '.join(reused) or '-'}")
    print(f"prompt changed or target exists, run fresh ({len(fresh)}): {', '.join(fresh) or '-'}")
    print("Re-grade the reused outputs; new evals need fresh baselines.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
