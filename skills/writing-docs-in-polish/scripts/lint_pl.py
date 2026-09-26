#!/usr/bin/env python3
"""Lint Polish Markdown documentation for typography, calques and register.

Usage:
    python scripts/lint_pl.py [--register publiczna|wewnetrzna] [--strict] PATH...

PATH may be a file or a directory (scanned recursively for *.md). Code blocks,
inline code, HTML comments, link targets and <placeholders> are ignored, so
commands and identifiers never trigger findings.

The register is taken from --register, or from a `Rejestr: wewnętrzna` marker
in the file, defaulting to `publiczna`. Jargon verbs are reported only in the
public register.

Exit status: 1 if any error was found (or any warning with --strict), else 0.
Stdlib only.
"""
import argparse
import re
import sys
from pathlib import Path

ERROR, WARNING = "error", "warning"

EM_DASH = "\u2014"
EN_DASH = "\u2013"

# (pattern, suggestion) for calques from references/style.md
CALQUES = [
    (r"\bposiada\w*", "use „ma”, „zawiera” (posiadać = legal ownership)"),
    (r"\bwspier\w*|\bwspiera\w*", "use „obsługuje” for software features"),
    (r"\bwsparci\w*", "use „obsługa” for software features (wsparcie = moral/financial support)"),
    (r"\bdedykowan\w*", "use „przeznaczony do”, „osobny”"),
    (r"\bw oparciu o\b", "use „na podstawie”"),
    (r"\bprzy pomocy\b", "use „za pomocą” for tools"),
    (r"\bbazuj\w* na\b", "use „opiera się na”"),
    (r"\badresow\w*", "use „rozwiązywać” (problem)"),
    (r"\baplikow\w* zmian", "use „wprowadzać zmiany”"),
    (r"\bkliknij na\b", "use „kliknij <element>” without „na”"),
    (r"\bpozwala ci na\b", "use „umożliwia” or „możesz”"),
    (r"\bw celu \w+enia\b", "use „aby + bezokolicznik”"),
    (r"\bserwis\w*", "use „usługa” or the English term (Service)"),
    (r"\bwolumin\w*|\bwolumen\w*", "use „volume”"),
    (r"\bmógłbyś\b|\bchciałbyś\b|\bmogłabyś\b|\bchciałabyś\b", "gender-forcing conditional; use „możesz”, „jeśli chcesz”"),
]

# English stems that become jargon verbs with Polish endings (zdeployuj, zmergował, upgrade'ować)
JARGON_STEMS = (
    "deploy|build|merg|rollback|commit|push|pull|rebase|squash|cherry-pick|provision|"
    "patch|upgrade|downgrade|backup|restor|trigger|fail|retry|releas|approv|drain|cordon|"
    "mock|stub|benchmark|harden|debug|refactor|scrap|ingest|forward|rout|throttl|"
    "fork|checkout|stash|restart|label|annotat|bootstrap"
)
JARGON_RE = re.compile(
    r"\b(?:z|s|ze|za|wy|prze|od|o)?(?:" + JARGON_STEMS + r")e?'?(?:ow|uj)\w*",
    re.IGNORECASE,
)

MINOR_WORDS = {
    "i", "a", "w", "z", "o", "u", "na", "do", "od", "po", "za", "ze", "we", "dla", "przez",
    "oraz", "lub", "albo", "czy", "nie", "jak", "bez", "pod", "nad", "przy", "the", "and",
}
VERSION_CONTEXT = re.compile(
    r"(wersj\w*|version|\bv|python|node|java|go|rfc|http|https|tls|ssl|openapi|oauth|semver|"
    r"rozdzia\w*|sekcj\w*|punkt\w*|krok\w*|§)[\s:]*$",
    re.IGNORECASE,
)


# A capitalized word (product name) or a token with digits right before the number: "Ubuntu 24.04"
PRODUCT_BEFORE = re.compile(r"(?:\b[A-ZĄĆĘŁŃÓŚŹŻ][\w+.-]*|\b\w*\d\w*)\s+$")

POSSESSIVE_RE = re.compile(r"\b(twój|twoja|twoje|twojego|twojej|twojemu|twoim|twoją|twoich|twoimi)\b")

# Notes addressed to whoever requested the document, not to its reader
WRITER_NOTE_HEADING = re.compile(r"^(założenia|uwagi do tłumaczenia|uwagi tłumacza|notatki dla autora)\b", re.IGNORECASE)
WRITER_NOTE_PHRASE = re.compile(r"\b(zleceni\w*|zlecając\w*|w poleceniu nie podano|prompt\w*)\b", re.IGNORECASE)

PLACEHOLDER_RE = re.compile(r"<[^<>\n]*[^\x00-\x7f][^<>\n]*>")


def check_code_placeholders(text, report):
    """Placeholders inside code must be ASCII so commands stay copy-pasteable."""
    in_fence = None
    in_comment = False
    for number, line in enumerate(text.splitlines(), 1):
        fence = re.match(r"^\s*(```|~~~)", line)
        if fence:
            in_fence = fence.group(1) if in_fence is None else (None if fence.group(1) == in_fence else in_fence)
            continue
        if not in_fence:
            if in_comment or "<!--" in line:
                in_comment = "-->" not in line.split("<!--")[-1] if "<!--" in line else "-->" not in line
                continue
        spans = [line] if in_fence else re.findall(r"`[^`]*`", line)
        for span in spans:
            for m in PLACEHOLDER_RE.finditer(span):
                report(number, line.find(m.group(0)), WARNING, "placeholder-ascii",
                       f"placeholder {m.group(0)} in code has non-ASCII characters; use ASCII snake_case")


def strip_markup(line):
    """Blank out spans that must not be linted, keeping column positions."""
    def blank(match):
        return " " * len(match.group(0))

    line = re.sub(r"`[^`]*`", blank, line)
    line = re.sub(r"\]\([^)]*\)", blank, line)
    line = re.sub(r"https?://\S+", blank, line)
    line = re.sub(r"<[^>\n]*>", blank, line)
    return line


def prose_lines(text):
    """Yield (line_number, original, cleaned) for lines that contain prose."""
    in_fence = None
    in_comment = False
    in_frontmatter = text.startswith("---\n")
    for number, line in enumerate(text.splitlines(), 1):
        if in_frontmatter:
            if number > 1 and line.strip() == "---":
                in_frontmatter = False
            continue
        fence = re.match(r"^\s*(```|~~~)", line)
        if fence:
            if in_fence is None:
                in_fence = fence.group(1)
            elif fence.group(1) == in_fence:
                in_fence = None
            continue
        if in_fence:
            continue

        cleaned = line
        if in_comment:
            end = cleaned.find("-->")
            if end == -1:
                continue
            cleaned = " " * (end + 3) + cleaned[end + 3:]
            in_comment = False
        cleaned = re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), cleaned)
        start = cleaned.find("<!--")
        if start != -1:
            cleaned = cleaned[:start]
            in_comment = True
        if re.match(r"^\s*\|?[\s:|-]+\|?\s*$", cleaned):
            continue  # table separator row
        yield number, line, strip_markup(cleaned)


def is_title_case(heading):
    words = re.findall(r"[^\W\d_][\w'-]*", heading)
    rest = [w for w in words[1:] if w.lower() not in MINOR_WORDS and len(w) > 2]
    if len(rest) < 2:
        return False
    # Title Case capitalizes every content word; one lowercase word means sentence
    # case with proper nouns ("Kopia zapasowa w PostgreSQL i Kubernetes").
    if any(w[0].islower() for w in rest):
        return False
    return sum(1 for w in rest if not w.isupper()) >= 2


def detect_register(text, override):
    if override:
        return override
    marker = re.search(r"Rejestr:\s*(publiczna|wewn[eę]trzna)", text, re.IGNORECASE)
    if marker and marker.group(1).lower().startswith("wewn"):
        return "wewnetrzna"
    return "publiczna"


def lint(path, register_override):
    text = path.read_text(encoding="utf-8")
    register = detect_register(text, register_override)
    findings = []

    def report(number, column, level, code, message):
        findings.append((path, number, column + 1, level, code, message))

    for number, line, prose in prose_lines(text):
        for m in re.finditer(EM_DASH, line):
            report(number, m.start(), ERROR, "em-dash", f"em dash (U+2014); use en dash „{EN_DASH}” (U+2013)")
        for m in re.finditer(r"(?<=\S) - (?=\S)", prose):
            report(number, m.start(), ERROR, "hyphen-dash", f"hyphen used as a dash; use spaced en dash „ {EN_DASH} ”")
        for m in re.finditer(r'"', prose):
            report(number, m.start(), ERROR, "straight-quote", "straight quote; use „…”")
        for m in re.finditer("“", prose):
            report(number, m.start(), ERROR, "english-quote", "English opening quote “; use „ (U+201E)")

        heading = re.match(r"^\s{0,3}#{1,6}\s+(.*)$", prose)
        if heading:
            title = heading.group(1).strip()
            if is_title_case(title):
                report(number, 0, WARNING, "title-case", "heading looks like Title Case; use sentence case")
            if title.endswith(".") and not re.fullmatch(r"[\d.\s]+", title):
                report(number, 0, WARNING, "heading-period", "heading ends with a full stop")
        else:
            for m in re.finditer(r"(?<![\w./])(\d+)\.(\d+)(?![\w.])", prose):
                before = prose[:m.start()]
                if not VERSION_CONTEXT.search(before) and not PRODUCT_BEFORE.search(before):
                    report(number, m.start(), WARNING, "decimal-point",
                           f"decimal point in {m.group(0)}; use a decimal comma ({m.group(1)},{m.group(2)}) unless it is a version")
        for m in re.finditer(r"(?<![\w,.])\d{1,3},\d{3}(?![\d,])", prose):
            report(number, m.start(), WARNING, "thousands-comma",
                   f"{m.group(0)} reads as a decimal in Polish; for thousands use a space or no separator")

        # Pronouns addressing the reader are lowercase in documentation (uppercase is for letters)
        for m in re.finditer(r"(?<=\w[ ,])(Twój|Twoja|Twoje|Twojego|Twojej|Twoim|Twoją|Twoich|Twoimi|Tobie|Ciebie|Ci)\b", prose):
            report(number, m.start(), WARNING, "pronoun-case",
                   f"„{m.group(0)}” mid-sentence; use lowercase in documentation")

        for m in POSSESSIVE_RE.finditer(prose):
            report(number, m.start(), WARNING, "possessive",
                   f"„{m.group(0)}” is often a calque of English „your”; drop it when ownership is obvious")

        if heading and WRITER_NOTE_HEADING.match(heading.group(1).strip()):
            report(number, 0, WARNING, "writer-note",
                   "section looks like a note for the requester; put assumptions in your reply, not in the document")
        for m in WRITER_NOTE_PHRASE.finditer(prose):
            report(number, m.start(), WARNING, "writer-note",
                   f"„{m.group(0)}” refers to the request, not the reader; move it to your reply")

        lowered = prose.lower()
        for pattern, suggestion in CALQUES:
            for m in re.finditer(pattern, lowered):
                report(number, m.start(), WARNING, "calque", f"„{prose[m.start():m.end()]}”: {suggestion}")

        if register == "publiczna":
            for m in JARGON_RE.finditer(prose):
                report(number, m.start(), WARNING, "jargon",
                       f"„{m.group(0)}” is developer jargon; public docs use Polish verbs (see polish-technical-vocabulary.md)")
    check_code_placeholders(text, report)
    return findings


def collect(paths):
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            yield from sorted(path.rglob("*.md"))
        else:
            yield path


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--register", choices=["publiczna", "wewnetrzna"],
                        help="override register detection (default: file marker, else publiczna)")
    parser.add_argument("--strict", action="store_true", help="exit with 1 on warnings too")
    args = parser.parse_args()

    findings = []
    for path in collect(args.paths):
        if not path.exists():
            print(f"{path}: not found", file=sys.stderr)
            return 2
        findings.extend(lint(path, args.register))

    for path, number, column, level, code, message in findings:
        print(f"{path}:{number}:{column}: {level} [{code}] {message}")

    errors = sum(1 for f in findings if f[3] == ERROR)
    warnings = len(findings) - errors
    print(f"{errors} error(s), {warnings} warning(s)", file=sys.stderr)
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
