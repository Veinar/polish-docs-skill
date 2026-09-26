#!/usr/bin/env python3
"""Look up terms in the skill's glossaries and print only the matching rows.

Usage:
    python scripts/term.py WORD [WORD ...] [--max N]

Searches the tables of references/terminology.md, polish-technical-vocabulary.md and
style.md (EN -> PL terms, jargon verbs per register, noun inflection, forms to avoid,
calques, GUI verbs). A word matches at the start of a word, so `deploy` finds
deployment and deployować. Use it instead of reading the glossaries: a lookup costs
tens of tokens, a whole file thousands. Stdlib only.
"""
import argparse
import re
import sys
from pathlib import Path

REFERENCES = Path(__file__).resolve().parent.parent / "references"
FILES = ("terminology.md", "polish-technical-vocabulary.md", "style.md")


def rows(path):
    """Yield (section, header, row) for every table data row."""
    section, header, in_table = path.stem, None, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            section, header, in_table = f"{path.stem} > {line.lstrip('#').strip()}", None, False
        elif line.startswith("|"):
            if re.match(r"^\|[\s:|-]+\|?$", line):
                in_table = True
            elif not in_table:
                header = line
            else:
                yield section, header, line
        else:
            in_table = False


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("words", nargs="+")
    parser.add_argument("--max", type=int, default=8, help="rows per word (default 8)")
    args = parser.parse_args()

    table = [(s, h, r) for name in FILES for s, h, r in rows(REFERENCES / name)]
    for word in args.words:
        pattern = re.compile(r"(?<!\w)" + re.escape(word), re.IGNORECASE)
        hits = [(s, h, r) for s, h, r in table if pattern.search(r)]
        if not hits:
            print(f"{word}: no entry. Keep the English term if it is the industry norm and inflect it; otherwise use an established Polish word.")
            continue
        last = None
        for section, header, row in hits[:args.max]:
            if section != last:
                print(f"[{section}] {header.strip('| ').replace(' | ', ' / ') if header else ''}")
                last = section
            print("  " + row.strip("| ").replace(" | ", " | "))
        if len(hits) > args.max:
            print(f"  ... {len(hits) - args.max} more for '{word}' (raise --max)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
