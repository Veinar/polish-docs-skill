---
name: writing-docs-in-polish
description: Writes, edits, reviews and translates technical documentation in Polish at the level of major open-source projects (Kubernetes, Pro Git, ArchWiki, PostgreSQL). Covers tutorials, how-to guides, concept pages, reference pages (CLI, SQL, API, man pages), specifications with RFC-style requirement keywords, README files, ADRs, changelogs, release notes, and internal engineering docs (runbooks, postmortems, PR descriptions) with natural Polish developer jargon. Use whenever the user asks for documentation "po polsku" or in Polish, writes a documentation request in Polish (e.g. "napisz dokumentację", "przygotuj README", "opisz API", "przetłumacz docs", "napisz instrukcję"), or asks to translate or proofread Polish docs. Not for "polishing" (refining) English text.
license: MIT
metadata:
  author: Veinar
  version: "0.5.0"
---

# Writing documentation in Polish

The goal is documentation that a Polish engineer reads as native technical prose – precise like PostgreSQL's reference, readable like Pro Git, task-focused like ArchWiki – never as a machine translation. The Kubernetes Polish localization guide puts it well: the text must not give the impression of being machine-translated.

Most failures in real Polish docs are of three kinds: calques from English syntax, English typography (Title Case, "quotes", decimal points), and inconsistent terminology (Pod/pod, polecenie/komenda). Everything below targets those.

## Workflow

Copy this checklist and track progress:

```
Postęp:
- [ ] 1. Rozpoznaj typ treści
- [ ] 2. Sprawdź konwencje projektu i ustal rejestr
- [ ] 3. Napisz według szablonu typu treści
- [ ] 4. Zweryfikuj język, terminologię i typografię
- [ ] 5. Uruchom lint_pl.py i przejdź listę kontrolną
```

**1. Identify the content type.** Each type has a different purpose and skeleton – mixing them (a tutorial that turns into a reference dump) is the most common structural flaw. Pick one:

| Type | Reader's question | Register | Template |
|---|---|---|---|
| Tutorial (samouczek) | "Naucz mnie" | publiczna | [tutorial.md](assets/templates/tutorial.md) |
| How-to (instrukcja) | "Jak zrobić X?" | either | [how-to.md](assets/templates/how-to.md) |
| Concept (koncepcja) | "Jak to działa i dlaczego?" | publiczna | [concept.md](assets/templates/concept.md) |
| CLI reference / man page | "Jakie są opcje?" | publiczna | [reference-cli.md](assets/templates/reference-cli.md) |
| SQL reference | "Jaka jest składnia?" | publiczna | [reference-sql.md](assets/templates/reference-sql.md) |
| API reference | "Co przyjmuje i zwraca?" | publiczna | [reference-api.md](assets/templates/reference-api.md) |
| Specification | "Co jest wymagane?" | publiczna | [specification.md](assets/templates/specification.md) |
| README | "Co to jest i jak zacząć?" | either | [readme.md](assets/templates/readme.md) |
| ADR | "Co i dlaczego zdecydowaliśmy?" | wewnętrzna | [adr.md](assets/templates/adr.md) |
| Changelog | "Co się zmieniło?" | publiczna | [changelog.md](assets/templates/changelog.md) |
| Runbook | "Co robić, gdy alert?" | wewnętrzna | [runbook.md](assets/templates/runbook.md) |
| Postmortem | "Co się stało i czego się nauczyliśmy?" | wewnętrzna | [postmortem.md](assets/templates/postmortem.md) |
| Pull request | "Co zmienia ten PR?" | wewnętrzna | [pull-request.md](assets/templates/pull-request.md) |
| Commit message | "Dlaczego ta zmiana?" | wewnętrzna | [commit-message.md](assets/templates/commit-message.md) |

Copy the template, fill it in, and delete the `<!-- … -->` guidance comments and any section that would stay empty. The rules that make each type work are in [references/content-types.md](references/content-types.md).

**2. Existing conventions win; choose the register.** If the project already has Polish docs or a glossary, match their register, terms and heading style. Consistency inside one project beats these defaults. Leave code comments and identifiers in the codebase's language unless asked otherwise.

**3. Write** using the template and the core rules below. For specifications, use [references/requirements-language.md](references/requirements-language.md).

**4. Verify language, terms and typography.** First list the document's key concepts and check each is named one way throughout (not "mikroserwisy" in one paragraph and "usługi" in the next; not "request" and "żądanie"). Then check against [references/style.md](references/style.md) (anti-calque catalogue and phrasebook), [references/terminology.md](references/terminology.md) and [references/typography.md](references/typography.md).

**5. Lint, then review.** Save the document as Markdown and run:

```bash
python scripts/lint_pl.py --register <publiczna|wewnetrzna> <plik.md>
```

(the path is relative to this skill's directory). It reports em dashes, hyphens used as dashes, straight or English quotes, Title Case headings, decimal points, English thousands separators, calques and – in the public register – jargon verbs. Fix every error; for each warning either fix it or confirm it is a false positive (e.g. a version number). Then go through the checklist below. Repeat until both pass.

## Core rules

**Pick the register first: publiczna or wewnętrzna.** Public product docs (the Kubernetes/PostgreSQL level) use Polish verbs – wdrożyć, zbudować, scalić – with established English nouns inflected (commit, pod, pipeline). Internal engineering docs (runbooks, postmortems, internal READMEs, PR descriptions) use the jargon Polish engineers actually write: "zdeployuj na staging", "build się wywalił", "zrollbackuj deployment". Forcing formal Polish into internal docs sounds stiff; jargon in public docs sounds careless. Details, spelling rules (z-/s-/ze- prefixes, apostrophes) and inflection tables: [references/polish-technical-vocabulary.md](references/polish-technical-vocabulary.md).

**Address the reader as "ty".** Kubernetes, Pro Git, ArchWiki and the Python docs all do. Imperative for steps ("Uruchom", "Sprawdź"), 3rd person for descriptions ("Polecenie zwraca…"). Pronouns lowercase ("twój", "ci"). Avoid "Państwo" and heavy "należy…" chains; one "należy" in a warning is fine.

**Gender-neutral by construction.** Avoid past-tense 2nd person forms that force a gender ("uruchomiłeś", "chciałbyś"). Rephrase instead of writing "(-aś)":
- "w terminalu, w którym uruchomiłeś `minikube start`" → "w terminalu, w którym działa `minikube start`"
- "Jeśli chciałbyś zautomatyzować…" → "Jeśli chcesz zautomatyzować…"

**Write Polish syntax, not English.** Drop redundant possessives ("your"), prefer active verbs, use "za pomocą" for tools, "ma" not "posiada", "obsługuje" not "wspiera". See the full catalogue in style.md.

**Headings in sentence case, no final full stop.** "Instalacja i usuwanie", never "Instalacja i Usuwanie". Step headings in tasks and tutorials are imperatives ("Zweryfikuj podpis"); concept and reference headings are nouns ("Komponenty klastra", "Parametry"). Keep one form per document.

**Code stays code.** Never translate identifiers, commands, flags, paths, config keys, API object kinds used as identifiers, or program output. Put them in backticks and inflect the surrounding words: "w pliku `config.yaml`", "zmienna `PATH`". When prose refers to English output or UI text, quote it and gloss once: „Untracked files” (nieśledzone pliki), „Running” (działa).

**Placeholders** in commands: `<nazwa_bazy>` in angle brackets, snake_case, ASCII-only so they stay copy-pasteable. Explain them once in a "Konwencje" section or right below the command.

**Terminology.** One term per concept for the whole document. Prefer established Polish terms; keep English where it is the industry norm and inflect it ("commita", "poda", "Kubernetesa"). Avoid phonetic polonizations such as "serwis" or "wolumin": use a real Polish word (usługa) or the English term. On first use of an ambiguous term, give the original: "warstwa sterowania (ang. *control plane*)".

**Dashes: en dash only.** Use the spaced en dash " – " (U+2013) as the sentence dash and the unspaced en dash for ranges (10–20). Never output an em dash (U+2014), even when the source text or an English original uses one.

**Numbers and typography**: „cudzysłów”, decimal comma (0,5 s), space as thousands separator (10 000), value and unit separated (512 MiB), dates "26 września 2026 r." or ISO `2026-09-26`.

**Don't invent facts silently.** When the request lacks details the document needs (names, versions, limits, UI labels), use placeholders (`<nazwa_usługi>`) or state what you assumed in a short "Założenia" section or callout. The reader must be able to tell given facts from guesses.

**Instructions must be executable.** One action per step, numbered. Put warnings before the step they concern, not after. After a step that changes state, say what the reader should see. Say what a command does not do when readers could reasonably assume it does (a rollback that does not revert migrations). GUI conventions and verbs: [references/style.md](references/style.md#gui-instructions).

**Translation mode.** The source text is authoritative. Translate everything that is prose. Don't leave English paragraphs behind (a half-translated chapter is worse than none). Record which source version was translated. Mark links that lead to English-only pages: "(w języku angielskim)".

## Example

Input: "Napisz instrukcję: jak zweryfikować podpis pobranego obrazu ISO."

Output:

````markdown
# Weryfikacja podpisu obrazu ISO

Sprawdzenie podpisu PGP potwierdza, że obraz nie został zmodyfikowany po opublikowaniu – szczególnie ważne przy pobieraniu z serwera lustrzanego.

## Zanim zaczniesz

- Zainstaluj GnuPG.
- Pobierz obraz ISO i plik podpisu `.sig` do tego samego katalogu.

## 1. Zweryfikuj podpis

```bash
gpg --keyserver-options auto-key-retrieve --verify obraz-<wersja>.iso.sig
```

Zastąp `<wersja>` numerem wersji pobranego obrazu.

Jeśli podpis jest prawidłowy, wynik zawiera wiersz podobny do poniższego:

```
gpg: Good signature from "Jan Kowalski <jan@example.org>"
```

> **Ostrzeżenie:** komunikat „Good signature” nie wystarcza, jeśli klucz nie jest zaufany. Porównaj odcisk palca klucza z odciskiem opublikowanym na stronie projektu.

## Co dalej

- Przygotuj nośnik instalacyjny.
````

## Review checklist

- [ ] One content type; structure follows its template
- [ ] Headings in sentence case; step headings are imperatives
- [ ] One register (publiczna / wewnętrzna) held throughout; jargon spelled per vocabulary rules
- [ ] Reader addressed as "ty"; no gender-forcing forms; no stray "Państwo"
- [ ] No calques from style.md's catalogue ("posiada", "wspiera", "w oparciu o", Title Case…)
- [ ] One term per concept; English terms inflected naturally
- [ ] Code, commands, output and identifiers untranslated, in backticks; output glossed where needed
- [ ] No em dash (U+2014) anywhere; dashes are en dashes only
- [ ] Polish quotes „…”, decimal commas, diacritics everywhere
- [ ] Every command has context: what it does, expected result, what to do on failure, what it does not undo
- [ ] Steps numbered, one action each; warnings precede the risky step
- [ ] No silently invented facts: placeholders or a „Założenia” section
- [ ] No leftover English prose; English-only links marked
- [ ] Matches conventions already present in the project
