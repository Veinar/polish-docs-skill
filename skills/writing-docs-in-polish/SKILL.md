---
name: writing-docs-in-polish
description: Writes, edits, translates and proofreads technical documentation in Polish at the level of Kubernetes, Pro Git, ArchWiki and PostgreSQL docs (tutorials, how-tos, references, specifications, READMEs, ADRs, runbooks, changelogs, PR and commit text). Use when the user wants docs "po polsku" or in Polish, asks in Polish for docs ("napisz instrukcję", "przetłumacz docs"), or wants Polish docs translated or proofread. Not for "polishing" English text.
license: MIT
metadata:
  author: Veinar
  version: "0.8.2"
---

# Writing documentation in Polish

Technically correct, usable documentation that reads as native Polish. Language rules serve the content.

## Priorities

When rules conflict, the higher one wins: 1 technical correctness and completeness; 2 safety and reversibility; 3 executable steps; 4 source fidelity; 5 project conventions and the user's own terms; 6 natural Polish; 7 consistent terminology; 8 typography. Never drop technical content for a language rule. Templates are structure, not a content limit. Never mention this skill in the document or the reply.

## Fast path

Small tasks (a paragraph, a few lines, one short section): apply the core rules directly. No template, scan or linter; read a reference only for a specific question. Deliver only the text. For translation or proofreading read `references/translation.md` first.

## Workflow (documents of a page or more)

1. **Type and register.** Copy a template from `assets/templates/`; its first-line comment gives the register and the type's rules.
   - publiczna: `tutorial`, `concept`, `reference-cli`, `reference-sql`, `reference-api`, `specification`, `changelog`
   - publiczna or inżynierska: `how-to`, `readme`
   - inżynierska: `adr`, `runbook`, `postmortem`
   - potoczna: `pull-request`, `commit-message`

   Registers: **publiczna** = external readers, Polish verbs (wdrożyć, zbudować), English nouns inflected. **inżynierska** = internal, engineers' jargon (zdeployuj, zrollbackuj), no slang. **potoczna** = PR, commit, chat: jargon and slang. Default publiczna; use inżynierska when the user says the text is for their team or internal ("pisz jak piszemy w zespole", "dla zespołu"). One register per document.
2. **Conventions.** With a repository run `python scripts/detect_conventions.py <repo>` and match its language, filename style and the case of identifiers and placeholders (snake_case, camelCase, kebab-case, PascalCase). Its glossary and the user's terms win over this skill; never rename them.
3. **Scope.** List what the reader needs: prerequisites, dependencies, side effects, limits, failure modes, verification, undo. For a translation: every warning, negation, value and example.
4. **Draft** from the template: fill it in, then delete every `<!-- … -->` comment and every empty section.
5. **Completeness.** Add what is missing, even beyond the template: every prerequisite named; every destructive step preceded by a warning and a way to check the current state; what the change does not undo; verification and rollback; likely failures; nothing from the source dropped or reversed (reread every negation and every "undecided" statement); no guess about a tool presented as fact.
6. **Lint.** `python scripts/lint_pl.py --fix --register <publiczna|inzynierska|potoczna> <file>` fixes dashes, quotes, ISO dates, leftover template comments and a mid-sentence "Twój", and lists the rest. Fix what is listed by hand in one pass (dismiss false positives), then deliver. Never loop.

Terms: `python scripts/term.py <word> ...` prints only the matching glossary rows (EN→PL, jargon per register, calques). Do not read the glossaries. Other references, only when needed: `references/content-types.md` (admonition labels, version notes), `references/requirements-language.md` (MUST/SHOULD in specs), `references/style.md` (GUI steps), `references/typography.md`.

## Core rules

- **Reader:** "ty"; imperative for steps, 3rd person for descriptions. Drop a redundant "twój" (reflexive "swój" only where it removes ambiguity). No past-tense forms that force a gender ("uruchomiłeś").
- **Polish syntax:** "ma" not "posiada", "obsługuje" not "wspiera", "za pomocą", "aby uruchomić…" not "w celu uruchomienia…".
- **Headings:** sentence case, no final full stop; imperatives for steps, nouns for concepts.
- **Steps:** numbered, one thing each (several clicks in one dialog may share a step); warnings before the risky step; say what the reader should see and what a command does not undo.
- **Code stays code:** never translate or invent identifiers, commands, flags or output; use backticks and inflect around them ("w pliku `config.yaml`").
- **Placeholders:** the project's case, else ASCII snake_case. In code: ASCII, no spaces. In prose (UI labels): `**<nazwa przycisku>**`. One style per document.
- **Terminology:** one term per concept; established Polish or inflected English (commita, poda). No "serwis" for *service* (use "usługa" or `Service`); "okno serwisowe" is fine. Give the original on first use of an ambiguous term.
- **Facts:** placeholders for missing details; never invent UI labels, menu names or paths (write **<nazwa opcji>**); assumptions go in your reply, not the file (an ADR or specification may have its own "Założenia i niewiadome"). A gap the user declared unknown stays unknown: no example values, no "defined elsewhere".
- **Deliver only the deliverable:** no source echo, notes or preface; for a file, a 2–3 line reply (path, assumptions, open points). The reply never describes how you worked (linter, register, templates, rules).
- **Dashes:** en dash only, spaced as a sentence dash, unspaced in ranges (10–20). Never an em dash, changelog headings included. Hyphens stay in ISO dates, compounds (klient-serwer), versions and identifiers.
- **Numbers and quotes:** decimal comma (0,5 s), space as thousands separator, space before units (512 MiB), dates "26 września 2026 r." or ISO; quotes „…”.
