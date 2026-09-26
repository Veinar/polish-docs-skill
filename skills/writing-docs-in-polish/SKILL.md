---
name: writing-docs-in-polish
description: Writes, edits, reviews and translates technical documentation in Polish at the level of major open-source projects (Kubernetes, Pro Git, ArchWiki, PostgreSQL). Covers tutorials, how-to guides, concept pages, reference pages (CLI, SQL, API, man pages), specifications with RFC-style requirement keywords, README files, ADRs, changelogs, release notes, and internal engineering docs (runbooks, postmortems, PR descriptions) with natural Polish developer jargon. Use whenever the user asks for documentation "po polsku" or in Polish, writes a documentation request in Polish (e.g. "napisz dokumentację", "przygotuj README", "opisz API", "przetłumacz docs", "napisz instrukcję"), or asks to translate or proofread Polish docs. Not for "polishing" (refining) English text.
license: MIT
metadata:
  author: Veinar
  version: "0.7.0"
---

# Writing documentation in Polish

The goal is documentation that is technically correct and usable, and that a Polish engineer reads as native prose rather than translation. Language rules serve the content, never the reverse.

## Priorities

When rules conflict, the higher one wins:

1. **Technical correctness and completeness**
2. **Safety and reversibility**
3. **Executability**: the reader can follow it step by step
4. **Source fidelity**: translation and proofreading keep every fact, warning, limit and negation
5. **Project conventions**: the user's and the repository's terms, naming and style beat this skill's defaults
6. **Natural Polish**
7. **Terminology consistency**
8. **Typography**

A language rule never justifies dropping technically relevant information. Templates give structure, not a content limit: add a section when the subject needs it. Natural Polish is not formal Polish: write the way a Polish engineer writes for that audience. Never mention this skill, its rules or its files in the document or in your reply.

## Workflow

```
Postęp:
- [ ] 1. Typ treści i rejestr
- [ ] 2. Konwencje projektu (detect_conventions.py)
- [ ] 3. Zakres techniczny
- [ ] 4. Szkic według szablonu
- [ ] 5. Przegląd kompletności technicznej
- [ ] 6. lint_pl.py --fix i poprawki
- [ ] 7. Lista kontrolna
```

**1. Content type and register.** Mixing types (a tutorial that turns into a reference dump) is the most common structural flaw.

| Type | Register | Template |
|---|---|---|
| Tutorial (samouczek) | publiczna | [tutorial.md](assets/templates/tutorial.md) |
| How-to (instrukcja) | publiczna or inżynierska | [how-to.md](assets/templates/how-to.md) |
| Concept (koncepcja) | publiczna | [concept.md](assets/templates/concept.md) |
| CLI reference / man page | publiczna | [reference-cli.md](assets/templates/reference-cli.md) |
| SQL reference | publiczna | [reference-sql.md](assets/templates/reference-sql.md) |
| API reference | publiczna | [reference-api.md](assets/templates/reference-api.md) |
| Specification | publiczna | [specification.md](assets/templates/specification.md) |
| README | publiczna (open source) or inżynierska (team) | [readme.md](assets/templates/readme.md) |
| Changelog | publiczna | [changelog.md](assets/templates/changelog.md) |
| ADR | inżynierska | [adr.md](assets/templates/adr.md) |
| Runbook | inżynierska | [runbook.md](assets/templates/runbook.md) |
| Postmortem | inżynierska | [postmortem.md](assets/templates/postmortem.md) |
| Pull request | potoczna | [pull-request.md](assets/templates/pull-request.md) |
| Commit message | potoczna | [commit-message.md](assets/templates/commit-message.md) |

Registers:
- **publiczna**: product docs, specifications, anything for external readers. Polish verbs (wdrożyć, zbudować, scalić), established English nouns inflected (commit, pod, pipeline).
- **inżynierska**: internal engineering docs. The jargon engineers write: "zdeployuj na staging", "zrollbackuj deployment". No slang.
- **potoczna**: PR descriptions, commit bodies, chat-like notes. As inżynierska, plus slang ("wywaliło się", "odpal").

Forcing formal Polish into internal docs sounds stiff; jargon in public docs sounds careless. Keep one register per document.

**2. Project conventions.** When there is a repository or the user points to one, run `python scripts/detect_conventions.py <katalog_repo>` (short output) and match what it reports: language and register of existing docs, filename style, and the naming case of identifiers and placeholders (snake_case, camelCase, kebab-case, PascalCase). Never force one case over the project's own. The project's glossary and the terms the user used win over this skill's terminology; do not rename them. With no signal, use the defaults below.

**3. Technical scope.** Before writing, list for yourself what the reader needs: components, prerequisites, dependencies, side effects, limits, failure modes, how to verify, how to undo. For translation and proofreading, list every warning, caveat, negation, value and example in the source.

**4. Draft.** Copy the template, fill it, delete the `<!-- … -->` comments and sections that would stay empty. Type-specific rules: [references/content-types.md](references/content-types.md).

**5. Completeness review.** Check the draft against the scope from step 3 and add what is missing, even beyond the template:
- every prerequisite and dependency named
- every destructive or hard-to-reverse step preceded by a warning and by a way to check the current state
- what the change does not undo or cover (a rollback that leaves database migrations)
- verification, and rollback or recovery
- failure modes readers are likely to hit
- nothing from the source dropped, softened or reversed (does not, unless, only, must not)
- statements about tools you are unsure of: verify, hedge or omit; never present a guess as fact

**6. Lint.** Run `python scripts/lint_pl.py --fix --register <publiczna|inzynierska|potoczna> <plik.md>`. It fixes mechanical typography itself (dashes, quotes) and lists the rest. Fix each remaining warning or confirm it as a false positive (version numbers, „okno serwisowe”). Run it at most twice.

**7. Checklist.**
- [ ] One type and register; structure follows the template plus what the subject needs
- [ ] Steps numbered, one thing each; warnings precede the risky step; expected results stated
- [ ] Nothing dropped from the source; no guesses presented as facts
- [ ] One term per concept; project terms kept
- [ ] Code, commands, output and identifiers untranslated and in backticks
- [ ] No notes for the requester inside the document; lint clean

Load references only when needed:

| Need | Read |
|---|---|
| Rules and sections for a content type, admonitions, version notes | [content-types.md](references/content-types.md) |
| Jargon verbs and inflection, per register | [polish-technical-vocabulary.md](references/polish-technical-vocabulary.md) (only your domain's section) |
| EN → PL term choice, the service/usługa decision tree | [terminology.md](references/terminology.md) (search for the term) |
| Translating or proofreading; lint reports calques; GUI steps | [style.md](references/style.md) |
| MUST / SHOULD / MAY in a specification | [requirements-language.md](references/requirements-language.md) |
| Lint reports typography you do not understand | [typography.md](references/typography.md) |

## Core rules

**Reader.** Address as "ty", imperative for steps ("Uruchom"), 3rd person for descriptions ("Polecenie zwraca…"). Drop "twój/twoja/twoje" where ownership is obvious ("Otwórz plik konfiguracyjny"); reflexive „swój” is fine only where it removes ambiguity. Avoid past-tense forms that force a gender ("uruchomiłeś", "chciałbyś"): rephrase ("w terminalu, w którym działa `minikube start`").

**Polish syntax, not English.** "ma" not "posiada", "obsługuje" not "wspiera", "za pomocą" for tools, "aby uruchomić…" not "w celu uruchomienia…". Full catalogue in style.md.

**Headings** in sentence case without a final full stop; steps and tasks use imperatives, concepts and references use nouns.

**Code stays code.** Never translate identifiers, commands, flags, paths, config keys, API object kinds or program output. Use backticks and inflect the words around them ("w pliku `config.yaml`"). Never invent a Polish form for an identifier. Quote English output or UI text and gloss it once: „Running” (działa).

**Placeholders and naming.** Match the project's case (`<databaseUrl>` in a camelCase project, `<nazwa_bazy>` in snake_case). With no signal, use ASCII snake_case. In code, placeholders are ASCII with no spaces so commands stay copy-pasteable. In prose, UI-label placeholders are written `**<nazwa przycisku>**`. Use one style per document and explain each placeholder once.

**Terminology.** One term per concept for the whole document. Prefer established Polish terms; keep English where it is the industry norm and inflect it ("commita", "poda"). Avoid "serwis" in the sense of *service* (use "usługa" or the English `Service`); "serwisowy" in the sense of maintenance ("okno serwisowe") is fine. Give the original on first use of an ambiguous term: "warstwa sterowania (ang. *control plane*)".

**Facts and requester notes.** When the request lacks details (names, versions, limits, UI labels), use placeholders so the reader can tell given facts from guesses. Report assumptions **in your reply**, not in the file: no "Założenia" or "Uwagi do tłumaczenia" sections written for the requester (an ADR or specification may have its own „Założenia i niewiadome”: that is content for the reader). The document may state reader-facing scope ("Instrukcja dotyczy serwerów z UEFI i Ubuntu 24.04."). If the user asks for a draft with open questions, use `<!-- DO UZUPEŁNIENIA: … -->`.

**Translation and proofreading.** The source is authoritative. Preserve meaning, prerequisites, warnings, limits, examples, command and API semantics, version constraints, order dependencies, negations and caveats; never shorten a technical source to make the Polish tidier. Translate all prose, localize numbers, gloss English-only UI labels once (**Settings** (Ustawienia)), record the source version, mark English-only links "(w języku angielskim)". Proofreading changes language, not content.

**Dashes: en dash only.** Spaced " – " as the sentence dash, unspaced for ranges (10–20). Never an em dash (U+2014), even when the source uses one. Changelog version headings follow the same rule: `## [1.2.0] – 2026-09-26`.

**Numbers.** Decimal comma (0,5 s), space as thousands separator (10 000), space before units (512 MiB), dates "26 września 2026 r." or ISO. Quotes are „…”.

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

Zastąp `<wersja>` numerem wersji pobranego obrazu. Jeśli podpis jest prawidłowy, wynik zawiera wiersz podobny do poniższego:

```
gpg: Good signature from "Jan Kowalski <jan@example.org>"
```

> **Ostrzeżenie:** komunikat „Good signature” nie wystarcza, jeśli klucz nie jest zaufany. Porównaj odcisk palca klucza z odciskiem opublikowanym na stronie projektu.

## Co dalej

- Przygotuj nośnik instalacyjny.
````
