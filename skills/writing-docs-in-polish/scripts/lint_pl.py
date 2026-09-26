#!/usr/bin/env python3
"""Lint Polish Markdown documentation for typography, calques, register and placeholders.

Usage:
    python scripts/lint_pl.py --register publiczna|inzynierska|potoczna [--fix] [--strict] PATH...

PATH may be a file or a directory (scanned recursively for *.md). Code blocks,
inline code, HTML comments, link targets and <placeholders> are ignored by the
prose checks, so commands and identifiers never trigger findings.

The register comes from --register or from a `Rejestr: <nazwa>` marker in the
file; without either the linter refuses to run, because jargon and slang rules
depend on it. Jargon verbs are reported in `publiczna`, slang outside `potoczna`.

--fix rewrites the mechanical typography problems in place (em dashes, hyphens
used as dashes, straight and English quotes) and then reports what remains.
--placeholder-style snake|camel|kebab|pascal enforces the project's naming case
for multi-word placeholders (default: only require consistency).
--ignore CODE[,CODE...] drops findings by code (e.g. placeholder-prose).

Exit status: 1 if any error remains (or any warning with --strict), 2 on usage
errors, else 0. Stdlib only.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ERROR, WARNING = "error", "warning"

EM_DASH = "\u2014"
EN_DASH = "–"
OPEN_QUOTE = "„"
CLOSE_QUOTE = "”"
ENGLISH_OPEN_QUOTE = "“"

REGISTERS = ("publiczna", "inzynierska", "potoczna")
REGISTER_ALIASES = {"wewnetrzna": "inzynierska", "wewnętrzna": "inzynierska", "inżynierska": "inzynierska"}
MAX_LINES = 40

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
    # "serwisowy" (maintenance: okno serwisowe) is correct; only the noun in the sense of *service* is flagged
    (r"\bserwis(?!ow)\w*", "in the sense of *service* use „usługa” or `Service` (maintenance and website senses are fine)"),
    (r"\bwolumin\w*|\bwolumen\w*", "use „volume”"),
    (r"\bmógłbyś\b|\bchciałbyś\b|\bmogłabyś\b|\bchciałabyś\b", "gender-forcing conditional; use „możesz”, „jeśli chcesz”"),
]

# English stems that become jargon verbs with Polish endings (zdeployuj, zmergował, upgrade'ować)
JARGON_STEMS = (
    "deploy|build|merg|rollback|commit|push|pull|rebase|squash|cherry-pick|provision|"
    "patch|upgrade|downgrade|backup|restor|trigger|fail|retry|releas|approv|drain|cordon|"
    "mock|stub|benchmark|harden|refactor|scrap|ingest|forward|rout|throttl|"
    "fork|checkout|stash|restart|label|annotat|bootstrap"
)
JARGON_RE = re.compile(
    r"\b(?:z|s|ze|za|wy|prze|od|o)?(?:" + JARGON_STEMS + r")e?'?(?:ow|uj)\w*",
    re.IGNORECASE,
)
SLANG_RE = re.compile(r"\b(?:wywali\w*|odpal\w*|ogarn\w*|przekop\w*|zaora\w*)", re.IGNORECASE)

MINOR_WORDS = {
    "i", "a", "w", "z", "o", "u", "na", "do", "od", "po", "za", "ze", "we", "dla", "przez",
    "oraz", "lub", "albo", "czy", "nie", "jak", "bez", "pod", "nad", "przy", "the", "and",
}
VERSION_CONTEXT = re.compile(
    r"(wersj\w*|version|\bv|python|node|java|go|rfc|http|https|tls|ssl|openapi|oauth|semver|"
    r"rozdzia\w*|sekcj\w*|punkt\w*|krok\w*|§)[\s:]*$",
    re.IGNORECASE,
)
# "wersji 4.7 do 4.8": a version keyword earlier in the same sentence (dots inside numbers do not end it)
VERSION_IN_SENTENCE = re.compile(r"\b(?:wersj\w*|version)\b(?:[^.!?;]|\.(?=\d))*$", re.IGNORECASE)
# A capitalized word (product name) or a token with digits right before the number: "Ubuntu 24.04"
PRODUCT_BEFORE = re.compile(r"(?:\b[A-ZĄĆĘŁŃÓŚŹŻ][\w+.-]*|\b\w*\d\w*)\s+$")

POSSESSIVE_RE = re.compile(r"\b(twój|twoja|twoje|twojego|twojej|twojemu|twoim|twoją|twoich|twoimi)\b")

# Notes addressed to whoever requested the document, not to its reader
WRITER_NOTE_HEADING = re.compile(r"^(uwagi do tłumaczenia|uwagi tłumacza|notatki (dla autora|techniczne|do tłumaczenia)|tekst źródłowy|komentarz tłumacza|podsumowanie (tłumaczenia|zmian))\b", re.IGNORECASE)
PROCESS_REMARK = re.compile(r"\bRejestr:|\bnegacje zachowan\w*|\bzachowan\w* (?:wszystk\w+ )?negacj\w*", re.IGNORECASE)
ASSUMPTIONS_HEADING = re.compile(r"^założenia\b(?! i niewiadome)", re.IGNORECASE)
WRITER_NOTE_PHRASE = re.compile(r"\b(zleceni\w*|zlecając\w*|w poleceniu nie podano|prompt\w*)\b", re.IGNORECASE)

PLACEHOLDER_RE = re.compile(r"<([^<>\n]+)>")
HTML_TAGS = {
    "br", "p", "div", "span", "details", "summary", "kbd", "code", "pre", "img", "a", "b", "i", "em",
    "strong", "table", "tr", "td", "th", "ul", "ol", "li", "hr", "sup", "sub", "picture", "source",
    "h1", "h2", "h3", "h4", "h5", "h6", "center", "thead", "tbody",
}
MULTI_WORD_STYLES = ("snake", "kebab", "camel", "pascal")
STYLE_LABEL = {"snake": "snake_case", "kebab": "kebab-case", "camel": "camelCase", "pascal": "PascalCase"}


# ---------------------------------------------------------------- scanning

def iter_lines(text):
    """Yield (number, in_fence, line, visible) for every body line.

    `visible` is the line with HTML comments blanked; frontmatter is skipped.
    """
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
            yield number, True, line, line
            continue
        visible = line
        if in_comment:
            end = visible.find("-->")
            if end == -1:
                continue
            visible = " " * (end + 3) + visible[end + 3:]
            in_comment = False
        visible = re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), visible)
        start = visible.find("<!--")
        if start != -1:
            visible = visible[:start]
            in_comment = True
        yield number, False, line, visible


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
    for number, in_fence, line, visible in iter_lines(text):
        if in_fence:
            continue
        if re.match(r"^\s*\|?[\s:|-]+\|?\s*$", visible):
            continue  # table separator row
        yield number, line, strip_markup(visible)


def prose_word_count(text):
    return sum(len(re.findall(r"\w+", prose)) for _, _, prose in prose_lines(text))


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


def resolve_register(text, override):
    """Return a canonical register or None when neither the flag nor a marker gives one."""
    if override:
        return REGISTER_ALIASES.get(override, override)
    marker = re.search(r"Rejestr:\s*(publiczna|in[zż]ynierska|potoczna|wewn[eę]trzna)", text, re.IGNORECASE)
    if not marker:
        return None
    name = marker.group(1).lower()
    return REGISTER_ALIASES.get(name, name)


# ------------------------------------------------------------ placeholders

def classify_placeholder(name):
    name = name.strip()
    if re.search(r"[^\x00-\x7f]", name):
        return "non-ascii"
    if " " in name:
        return "space-cap" if name[0].isupper() else "space"
    if re.fullmatch(r"[A-Z0-9]+(?:_[A-Z0-9]+)*", name):
        return "upper"
    if re.fullmatch(r"[a-z0-9]+", name):
        return "single"
    if re.fullmatch(r"[A-Za-z0-9]+(?:_[A-Za-z0-9]+)+", name):
        return "snake"
    if re.fullmatch(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+", name):
        return "kebab"
    if re.fullmatch(r"[a-z][a-z0-9]*(?:[A-Z][a-z0-9]*)+", name):
        return "camel"
    if re.fullmatch(r"(?:[A-Z][a-z0-9]*){2,}", name):
        return "pascal"
    return "other"


def is_placeholder(name):
    stripped = name.strip()
    if not stripped or stripped[0] in "/!?" or "://" in stripped or "@" in stripped or "=" in stripped:
        return False
    if stripped.split()[0].lower() in HTML_TAGS:
        return False
    return not re.search(r"[.,:;„”\"'()]", stripped)  # free text or examples, not a name


def placeholder_occurrences(text):
    """Yield (line, column, name, in_code) for every <placeholder> outside HTML comments."""
    for number, in_fence, line, visible in iter_lines(text):
        if in_fence:
            segments = [(0, line, True)]
        else:
            segments = []
            masked = visible
            for m in re.finditer(r"`[^`]*`", visible):
                segments.append((m.start(), m.group(0), True))
                masked = masked[:m.start()] + " " * len(m.group(0)) + masked[m.end():]
            masked = re.sub(r"\]\([^)]*\)|https?://\S+", lambda m: " " * len(m.group(0)), masked)
            segments.append((0, masked, False))
        for offset, segment, in_code in segments:
            for m in PLACEHOLDER_RE.finditer(segment):
                if is_placeholder(m.group(1)):
                    yield number, offset + m.start(), m.group(1), in_code


def check_placeholders(text, report, wanted_style):
    code, prose = [], []
    for number, column, name, in_code in placeholder_occurrences(text):
        (code if in_code else prose).append((number, column, name, classify_placeholder(name)))

    for number, column, name, style in code:
        if style == "non-ascii":
            report(number, column, WARNING, "placeholder-ascii",
                   f"placeholder <{name}> in code has non-ASCII characters; use ASCII")
        elif style in ("space", "space-cap"):
            report(number, column, WARNING, "placeholder-space",
                   f"placeholder <{name}> in code contains spaces; commands would not be copy-pasteable")
        elif wanted_style != "auto" and style in MULTI_WORD_STYLES and style != wanted_style:
            report(number, column, WARNING, "placeholder-style",
                   f"<{name}> is {STYLE_LABEL[style]}; the project uses {STYLE_LABEL[wanted_style]}")

    if wanted_style == "auto":
        used = Counter(s for _, _, _, s in code if s in MULTI_WORD_STYLES)
        if len(used) > 1:
            main = used.most_common(1)[0][0]
            first = next(o for o in code if o[3] in MULTI_WORD_STYLES and o[3] != main)
            summary = ", ".join(f"{STYLE_LABEL[s]} x{n}" for s, n in used.most_common())
            report(first[0], first[1], WARNING, "placeholder-style",
                   f"mixed placeholder styles in code ({summary}); use one")

    # In prose, UI-label placeholders use spaces (**<nazwa przycisku>**); one form per document
    forms = Counter(s for _, _, _, s in prose if s in ("space", "space-cap") + MULTI_WORD_STYLES)
    if len(forms) > 1:
        main = forms.most_common(1)[0][0]
        first = next(o for o in prose if o[3] in forms and o[3] != main)
        summary = ", ".join(f"{k} x{n}" for k, n in forms.most_common())
        report(first[0], first[1], WARNING, "placeholder-prose",
               f"mixed placeholder forms in prose ({summary}); use one, e.g. **<nazwa przycisku>**")


# ------------------------------------------------------------------- lint

def lint(path, register, placeholder_style="auto"):
    text = path.read_text(encoding="utf-8")
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
        for m in re.finditer(ENGLISH_OPEN_QUOTE, prose):
            report(number, m.start(), ERROR, "english-quote", f"English opening quote {ENGLISH_OPEN_QUOTE}; use {OPEN_QUOTE} (U+201E)")

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
                if not (VERSION_CONTEXT.search(before) or PRODUCT_BEFORE.search(before) or VERSION_IN_SENTENCE.search(before)):
                    report(number, m.start(), WARNING, "decimal-point",
                           f"decimal point in {m.group(0)}; use a decimal comma ({m.group(1)},{m.group(2)}) unless it is a version")
        for m in re.finditer(r"(?<![\w,.])\d{1,3},\d{3}(?![\d,])", prose):
            report(number, m.start(), WARNING, "thousands-comma",
                   f"{m.group(0)} reads as a decimal in Polish; for thousands use a space or no separator")

        # Pronouns addressing the reader are lowercase in documentation (uppercase is for letters)
        for m in re.finditer(r"(?<=\w[ ,])(Twój|Twoja|Twoje|Twojego|Twojej|Twoim|Twoją|Twoich|Twoimi|Tobie|Ciebie|Ci)\b", prose):
            report(number, m.start(), WARNING, "pronoun-case", f"„{m.group(0)}” mid-sentence; use lowercase in documentation")
        for m in POSSESSIVE_RE.finditer(prose):
            report(number, m.start(), WARNING, "possessive",
                   f"„{m.group(0)}” is often a calque of English „your”; drop it when ownership is obvious")

        if heading and WRITER_NOTE_HEADING.match(heading.group(1).strip()):
            report(number, 0, WARNING, "writer-note",
                   "section looks like a note for the requester; put assumptions in your reply, not in the document")
        if heading and ASSUMPTIONS_HEADING.match(heading.group(1).strip()):
            report(number, 0, WARNING, "assumptions-section",
                   "„Założenia” is content in an ADR or specification; in other documents assumptions belong in your reply")
        for m in PROCESS_REMARK.finditer(prose):
            report(number, m.start(), WARNING, "process-remark",
                   f"„{m.group(0)}” describes how the text was produced; deliver only the document")
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
                       f"„{m.group(0)}” is developer jargon; publiczna register uses Polish verbs (polish-technical-vocabulary.md)")
        if register != "potoczna":
            for m in SLANG_RE.finditer(prose):
                report(number, m.start(), WARNING, "slang", f"„{m.group(0)}” is slang; allowed only in the potoczna register")

    check_placeholders(text, report, placeholder_style)
    return findings


# -------------------------------------------------------------------- fix

def fix_text(text):
    """Apply mechanical typography fixes. Returns (new_text, Counter of fixes)."""
    counts = Counter()
    lines = text.splitlines(keepends=True)
    for number, line, prose in prose_lines(text):
        body = line.rstrip("\r\n")
        edits = []  # (start, end, replacement)

        for m in re.finditer(EM_DASH, prose):
            start, end = m.start(), m.end()
            while start > 0 and body[start - 1] in " \t":
                start -= 1
            while end < len(body) and body[end] in " \t":
                end += 1
            spaced = start > 0 and end < len(body)
            edits.append((start, end, f" {EN_DASH} " if spaced else EN_DASH))
            counts["em dash"] += 1
        for m in re.finditer(r"(?<=\S) - (?=\S)", prose):
            edits.append((m.start(), m.end(), f" {EN_DASH} "))
            counts["hyphen dash"] += 1
        for m in re.finditer(ENGLISH_OPEN_QUOTE, prose):
            edits.append((m.start(), m.end(), OPEN_QUOTE))
            counts["English quote"] += 1
        straight = [m.start() for m in re.finditer(r'"', prose)]
        if straight and len(straight) % 2 == 0:
            for index, position in enumerate(straight):
                edits.append((position, position + 1, OPEN_QUOTE if index % 2 == 0 else CLOSE_QUOTE))
                counts["straight quote"] += 1

        if not edits:
            continue
        for start, end, replacement in sorted(edits, reverse=True):
            body = body[:start] + replacement + body[end:]
        original = lines[number - 1]
        lines[number - 1] = body + original[len(original.rstrip("\r\n")):]
    return "".join(lines), counts


# ------------------------------------------------------------------- main

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
    parser.add_argument("--register", choices=REGISTERS + tuple(REGISTER_ALIASES),
                        help="publiczna | inzynierska | potoczna (or a `Rejestr:` marker in the file)")
    parser.add_argument("--fix", action="store_true", help="fix mechanical typography in place, then report the rest")
    parser.add_argument("--strict", action="store_true", help="exit with 1 on warnings too")
    parser.add_argument("--placeholder-style", default="auto", choices=("auto",) + MULTI_WORD_STYLES,
                        help="naming case of multi-word placeholders in code (default: only require consistency)")
    parser.add_argument("--ignore", default="", help="comma-separated finding codes to drop")
    args = parser.parse_args()
    ignored = {code.strip() for code in args.ignore.split(",") if code.strip()}

    findings = []
    for path in collect(args.paths):
        if not path.exists():
            print(f"{path}: not found", file=sys.stderr)
            return 2
        with path.open(encoding="utf-8", newline="") as handle:
            text = handle.read()  # keep the file's own line endings
        register = resolve_register(text, args.register)
        if register is None:
            print(f"{path}: no register. Pass --register publiczna|inzynierska|potoczna "
                  f"(or add a `Rejestr:` marker).", file=sys.stderr)
            return 2
        if args.fix:
            fixed, counts = fix_text(text)
            if fixed != text:
                with path.open("w", encoding="utf-8", newline="") as handle:
                    handle.write(fixed)
                print(f"{path}: fixed " + ", ".join(f"{n} {name}" for name, n in counts.items()))
        findings.extend(f for f in lint(path, register, args.placeholder_style) if f[4] not in ignored)

    multi = len({f[0] for f in findings}) > 1
    seen = set()
    shown = 0
    for path, number, column, level, code, message in findings:
        key = (path, code, message)
        if key in seen:
            continue  # the same finding repeated on later lines adds nothing new
        seen.add(key)
        if shown < MAX_LINES:
            where = f"{path}:{number}" if multi else f"{number}"
            print(f"{where}: {level} [{code}] {message}")
            shown += 1
    if len(seen) > shown:
        print(f"... {len(seen) - shown} more distinct finding(s) not shown")

    errors = sum(1 for f in findings if f[3] == ERROR)
    warnings = len(findings) - errors
    print(f"{errors} error(s), {warnings} warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
