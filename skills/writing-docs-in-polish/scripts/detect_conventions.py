#!/usr/bin/env python3
"""Detect the writing and naming conventions of a repository so new docs match them.

Usage:
    python scripts/detect_conventions.py [ROOT] [--json]

Reports, in a short summary: language and typography of existing docs (quotes,
dashes, heading case, register hints), filename style, identifier style per source
language (snake_case, camelCase, kebab-case, PascalCase), config-key style,
placeholder style in existing docs and glossary or style-guide files. Ends with the
flags to pass to lint_pl.py. Stdlib only; scans at most 400 files.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint_pl  # noqa: E402  (shared classification helpers)

SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".venv", "venv", "__pycache__",
             "target", ".next", ".idea", ".vscode", "site-packages", "coverage", ".tox", ".mypy_cache"}
DOC_EXT = {".md", ".mdx", ".rst", ".adoc"}
CODE_EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".kt", ".rb", ".php", ".cs", ".swift", ".sh"}
CONFIG_EXT = {".yml", ".yaml", ".json", ".toml"}
CONVENTIONAL_UPPER = {"README", "CHANGELOG", "LICENSE", "CONTRIBUTING", "CODE_OF_CONDUCT", "SECURITY", "NOTICE", "AUTHORS", "TODO", "VERSION"}
MAX_FILES = 400
MAX_BYTES = 200_000
STYLE_LABEL = dict(lint_pl.STYLE_LABEL, upper="UPPER_SNAKE", single="single word")
PL_WORDS = {"się", "jest", "nie", "dla", "oraz", "który", "można", "jak", "przy", "tego", "lub", "czy"}
EN_WORDS = {"the", "and", "is", "for", "to", "of", "with", "this", "that", "you", "are", "can"}
DECLARATION = re.compile(r"\b(?:def|function|fn|func|const|let|var|val|class|struct|interface|type|enum)\s+([A-Za-z_][A-Za-z0-9_]*)")
CONFIG_KEY = re.compile(r'^\s*"?([A-Za-z_][A-Za-z0-9_-]*)"?\s*[:=]')
GLOSSARY_NAME = re.compile(r"glossary|slownik|słownik|terminolog|style[-_ ]?guide|styleguide|contributing", re.IGNORECASE)


def style_of(name):
    """Classify a multi-word or single identifier: snake, kebab, camel, pascal, upper, single, other."""
    return lint_pl.classify_placeholder(name)


def walk(root):
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.endswith("-workspace"))
        for filename in sorted(filenames):
            count += 1
            if count > MAX_FILES:
                return
            yield Path(dirpath) / filename


def read(path):
    try:
        if path.stat().st_size > MAX_BYTES:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def majority(counter, keep=("snake", "kebab", "camel", "pascal")):
    filtered = Counter({k: v for k, v in counter.items() if k in keep})
    if not filtered:
        return None, 0, 0
    style, n = filtered.most_common(1)[0]
    return style, n, sum(filtered.values())


def detect(root):
    root = Path(root)
    docs, doc_names, glossaries = [], Counter(), []
    identifiers = defaultdict(Counter)
    config_keys = defaultdict(Counter)
    ecosystems = set()
    scanned = 0

    for path in walk(root):
        scanned += 1
        ext = path.suffix.lower()
        rel = path.relative_to(root).as_posix()
        if path.name in {"package.json", "pyproject.toml", "go.mod", "Cargo.toml", "pom.xml", "Gemfile", "composer.json"}:
            ecosystems.add(path.name)
        if GLOSSARY_NAME.search(path.stem) and ext in DOC_EXT:
            glossaries.append(rel)
        if ext in DOC_EXT:
            stem = path.stem
            if stem not in CONVENTIONAL_UPPER:
                doc_names[style_of(stem)] += 1
            docs.append((rel, read(path)))
        elif ext in CODE_EXT:
            for name in DECLARATION.findall(read(path)):
                if name[0].islower():  # variables and functions; classes are PascalCase by convention
                    identifiers[ext][style_of(name)] += 1
        elif ext in CONFIG_EXT:
            for line in read(path).splitlines():
                m = CONFIG_KEY.match(line)
                if m:
                    config_keys[ext][style_of(m.group(1))] += 1

    result = {"root": str(root), "files_scanned": min(scanned, MAX_FILES), "docs": len(docs)}

    # Existing documentation: language, typography, register hints, placeholders
    languages, quotes, dashes, headings, jargon, placeholders = Counter(), Counter(), Counter(), Counter(), Counter(), Counter()
    for rel, text in docs:
        words = re.findall(r"[^\W\d_]+", text.lower())
        pl = sum(1 for w in words if w in PL_WORDS) + len(re.findall(r"[ąćęłńóśźż]", text.lower())) // 10
        en = sum(1 for w in words if w in EN_WORDS)
        language = "pl" if pl > en else "en"
        languages[language] += 1
        for _, _, name, in_code in lint_pl.placeholder_occurrences(text):
            if in_code:
                placeholders[style_of(name)] += 1
        if language != "pl":
            continue
        for _, _, prose in lint_pl.prose_lines(text):
            quotes["„…”"] += prose.count("„")
            quotes['"…"'] += prose.count('"')
            dashes["en dash"] += prose.count("–")
            dashes["em dash"] += prose.count("\u2014")
            dashes["spaced hyphen"] += len(re.findall(r"(?<=\S) - (?=\S)", prose))
            heading = re.match(r"^\s{0,3}#{1,6}\s+(.*)$", prose)
            if heading:
                headings["title case" if lint_pl.is_title_case(heading.group(1)) else "sentence case"] += 1
            for m in lint_pl.JARGON_RE.finditer(prose):
                jargon[m.group(0).lower()] += 1
    result["doc_languages"] = dict(languages)
    result["doc_filename_style"] = majority(doc_names)[0]
    result["doc_filename_counts"] = dict(doc_names)
    result["polish_typography"] = {"quotes": dict(quotes), "dashes": dict(dashes), "headings": dict(headings)}
    result["jargon_verbs"] = dict(jargon.most_common(5))
    result["placeholder_style"] = majority(placeholders)[0]
    result["placeholder_counts"] = dict(placeholders)
    result["glossary_files"] = glossaries[:5]
    result["identifier_style"] = {e: majority(c)[0] for e, c in identifiers.items() if majority(c)[0]}
    result["identifier_counts"] = {e: majority(c)[1] for e, c in identifiers.items() if majority(c)[0]}
    result["config_key_style"] = {e: majority(c)[0] for e, c in config_keys.items() if majority(c)[0]}
    result["ecosystems"] = sorted(ecosystems)

    # Recommendation
    if result["placeholder_style"]:
        recommended, reason = result["placeholder_style"], "existing docs"
    elif result["identifier_style"]:
        top_ext = max(result["identifier_counts"], key=result["identifier_counts"].get)
        recommended, reason = result["identifier_style"][top_ext], f"{top_ext} identifiers"
    else:
        recommended, reason = "snake", "no signal, default"
    result["recommended_placeholder_style"] = recommended
    result["placeholder_reason"] = reason
    if languages.get("pl"):
        result["register_hint"] = "inzynierska" if sum(jargon.values()) >= 2 else "publiczna"
    else:
        result["register_hint"] = None
    return result


def render(r):
    lines = [f"Repo: {r['root']} ({r['files_scanned']} files scanned)"]
    if not r["docs"]:
        lines.append("Docs: none found, so there is no documentation convention to match")
    else:
        langs = ", ".join(f"{k} {v}" for k, v in sorted(r["doc_languages"].items()))
        lines.append(f"Docs: {r['docs']} files; language {langs}")
    if r["doc_filename_style"]:
        lines.append(f"Doc filenames: {STYLE_LABEL[r['doc_filename_style']]} (counts {r['doc_filename_counts']})")
    typo = r["polish_typography"]
    if any(typo["quotes"].values()) or typo["headings"]:
        lines.append(f"Polish docs: quotes {typo['quotes']}; dashes {typo['dashes']}; headings {typo['headings']}")
    if r["register_hint"]:
        jargon = ", ".join(f"{k} x{v}" for k, v in r["jargon_verbs"].items()) or "none"
        lines.append(f"Register hint: {r['register_hint']} (jargon verbs in existing docs: {jargon})")
    if r["identifier_style"]:
        parts = [f"{e} {STYLE_LABEL[s]} (n={r['identifier_counts'][e]})" for e, s in r["identifier_style"].items()]
        lines.append("Identifiers: " + "; ".join(parts))
    if r["config_key_style"]:
        lines.append("Config keys: " + "; ".join(f"{e} {STYLE_LABEL[s]}" for e, s in r["config_key_style"].items()))
    if r["placeholder_style"]:
        lines.append(f"Placeholders in docs: {STYLE_LABEL[r['placeholder_style']]} ({r['placeholder_counts']})")
    if r["glossary_files"]:
        lines.append("Glossary or style files (read and follow): " + ", ".join(r["glossary_files"]))
    style = r["recommended_placeholder_style"]
    lines.append(f"=> Placeholder and example-identifier case: {STYLE_LABEL[style]} ({r['placeholder_reason']}); "
                 f"lint flag: --placeholder-style {style}")
    if r["doc_filename_style"]:
        lines.append(f"=> Name new doc files in {STYLE_LABEL[r['doc_filename_style']]}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()
    if not os.path.isdir(args.root):
        print(f"{args.root}: not a directory", file=sys.stderr)
        return 2
    result = detect(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
