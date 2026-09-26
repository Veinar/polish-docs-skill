#!/usr/bin/env python3
"""Pick a small random sample of evals so an iteration costs a fraction of the full set.

Usage:
    python scripts/pick_evals.py [--n 5] [--seed S] [--tag TAG] [--pin ID ...]
                                 [--workspace skills/writing-docs-in-polish-workspace]

Selection rules: evals that were run in fewer earlier iterations come first (so every
eval eventually gets sampled), ties prefer evals that add a tag not yet covered by the
sample, remaining ties are random. --pin forces evals in (e.g. one you just changed).
The seed is printed so a sample can be reproduced. Stdlib only.
"""
import argparse
import json
import random
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def previous_runs(workspace):
    counts = {}
    for iteration in Path(workspace).glob("iteration-*"):
        for eval_dir in iteration.glob("eval-*"):
            match = re.match(r"eval-(\d+)(?:-|$)", eval_dir.name)
            if match and any(eval_dir.rglob("*.md")):
                counts[int(match.group(1))] = counts.get(int(match.group(1)), 0) + 1
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--tag")
    parser.add_argument("--pin", type=int, nargs="*", default=[])
    parser.add_argument("--evals", default=str(ROOT / "evals" / "evals.json"))
    parser.add_argument("--workspace", default=str(ROOT / "skills" / "writing-docs-in-polish-workspace"))
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else int(time.time()) % 100000
    rng = random.Random(seed)
    evals = {e["id"]: e for e in json.loads(Path(args.evals).read_text(encoding="utf-8"))["evals"]}
    unknown = [i for i in args.pin if i not in evals]
    if unknown:
        print(f"unknown eval ids: {unknown}", file=sys.stderr)
        return 2
    runs = previous_runs(args.workspace)
    pool = [i for i, e in evals.items() if not args.tag or args.tag in e.get("tags", [])]
    chosen = list(dict.fromkeys(args.pin))
    covered = {tag for i in chosen for tag in evals[i].get("tags", [])}
    while len(chosen) < args.n and len(chosen) < len(pool):
        candidates = [i for i in pool if i not in chosen]
        rng.shuffle(candidates)
        best = min(candidates, key=lambda i: (runs.get(i, 0), -len(set(evals[i].get("tags", [])) - covered)))
        chosen.append(best)
        covered |= set(evals[best].get("tags", []))

    chosen.sort()
    for i in chosen:
        e = evals[i]
        print(f"eval {i:>2} [{e.get('register', '?'):11}] runs so far {runs.get(i, 0)}  tags {','.join(e.get('tags', []))}")
    print(f"\nids: {' '.join(map(str, chosen))}   (seed {seed}, {len(chosen)} of {len(evals)} evals)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
