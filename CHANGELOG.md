# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versioning follows [SemVer](https://semver.org/).

## [Unreleased]

## [0.8.0] – 2026-09-26

### Added
- `scripts/term.py`: prints only the matching rows of the glossaries (terms, jargon per register, calques, GUI verbs), so a lookup costs tens of tokens instead of thousands.
- `references/translation.md`: translation and proofreading rules and the negation table, read only for those tasks.
- Validator guards: `SKILL.md` at most about 2.5 k tokens, description at most 600 characters, every path and template mentioned in `SKILL.md` must exist.

### Changed
- `SKILL.md` rewritten to about 2 k tokens (was 3.2 k): terse priorities and core rules, one workflow, glossaries reached through `term.py` instead of being read.
- `content-types.md` keeps only shared elements (admonitions, version notes, cross-references); the per-type rules live in the template comments. The how-to and specification templates gained the rules that were only in `content-types.md`.
- Templates no longer repeat the „structure, not a content limit” note.

## [0.7.1] – 2026-09-26

### Added
- Fast path in SKILL.md: small tasks (a paragraph, a few lines) skip the workflow, templates, references and linter.
- Output discipline: deliver only the requested text (no source echo, no notes about what was preserved); the reply for a file is two or three lines.
- `scripts/pick_evals.py`: seeded random sample of evals; prefers evals with fewer earlier runs and spreads tags. Evals are never run as a full set.
- Linter: `process-remark` (Rejestr:, „negacje zachowane”) and more leaked meta headings (Notatki techniczne, Tekst źródłowy).

### Changed
- SKILL.md is about 3.2 k tokens (was 4.0 k): compact description and template list, checklist and example removed; content-types.md is no longer read by default.
- „Debugowanie” is no longer flagged as jargon in public docs; versions in one sentence („z wersji 4.7 do 4.8”) are not decimals.
- `lint_metrics.py` and `reuse_baselines.py` accept run directories without a slug or `run-1` level.

## [0.7.0] – 2026-09-26

### Added
- Priority order in SKILL.md: technical correctness, safety, executability, source fidelity and project conventions outrank language and typography. Language rules never justify dropping technical content.
- Technical scope and completeness-review steps in the workflow; templates are structure, not a content limit.
- Source fidelity rules for translation and proofreading (negations, limits, caveats), plus a negation table in `style.md`.
- `scripts/detect_conventions.py`: detects language, typography, register hints, filename style, identifier case (snake_case, camelCase, kebab-case, PascalCase), config-key case and placeholder case of a repository; output is short and ends with the flags to use. Placeholders and file names now match the project instead of forcing snake_case.
- `lint_pl.py`: `--fix` auto-corrects em dashes, hyphens used as dashes, straight and English quotes, keeping line endings; `--placeholder-style`, `--ignore`; checks for mixed placeholder styles, spaces in code placeholders, mixed prose placeholder forms, slang; duplicate findings are collapsed and output is capped.
- Third register `potoczna` (PR descriptions, commit bodies); `wewnętrzna` is renamed `inżynierska`. Slang is allowed only in `potoczna`.
- Terminology decision tree for *service* (identifier, microservice, register, maintenance sense).
- Dev tooling: `scripts/lint_metrics.py` (findings per 1000 words per iteration), `scripts/reuse_baselines.py` (reuse baseline runs when the prompt and model are unchanged), unit tests for the linter, `VERSION` and template-register checks in `validate_skills.py`, `evals/README.md`.
- 26 new evals (ids 14–39): 20 written by the owner on technical fidelity (negations, MUST/MAY, defaults, invented values, hypotheses vs proven causes, destructive steps, GitOps constraints) and 6 more covering contradictory source, proofreading, service terminology, repository conventions (fixture `evals/fixtures/ts-cli`), domain completeness (nginx TLS rotation) and table fidelity. Every eval has a `register` and `tags`.

### Changed
- `lint_pl.py` requires `--register` or a `Rejestr:` marker (no silent default).
- SKILL.md loads references on demand (table) instead of asking for all of them; workflow step 6 runs `--fix`, at most twice.
- „Serwis” is flagged only in the sense of *service*; „okno serwisowe” and „mikroserwis” are fine.
- „Rolling update” is „aktualizacja krocząca”; „staged/phased” is „wdrożenie etapowe”.
- Reflexive „swój” is allowed where it removes ambiguity.
- Template code placeholders are ASCII with no spaces.
- Removed eval checks that the linter measures objectively (sentence case, em dashes, quotes).
- „Założenia” headings get a softer warning (`assumptions-section`): they are content in an ADR or specification. The ADR template has an optional „Założenia i niewiadome” section.

## [0.6.0] – 2026-09-26

### Changed
- Assumptions and notes for the requester go in the reply, not in the document; documents may state reader-facing scope. The how-to template's „Założenia” section is removed.
- Step rule clarified: one thing done in one place; a few clicks in the same dialog may share a step.
- Drop redundant „twój/twoja/twoje” (English „your” calque).
- How-to rules: cover likely variants (BIOS/UEFI, versions) or state scope; include steps that make system changes durable.
- Template placeholders in code are ASCII-only.
- Eval 12 replaced with a harder source text; checks for leaked requester notes and possessives added to evals 6, 8–13.

### Added
- Linter checks: leaked requester notes (`writer-note`), redundant possessives (`possessive`), non-ASCII placeholders in code (`placeholder-ascii`).

### Fixed
- Linter no longer flags product versions such as „Ubuntu 24.04” or „Helm 3.12” as decimals.

## [0.5.0] – 2026-09-26

### Added
- Rules for executable instructions: numbered steps, one action per step, warnings before the risky step, stating what a command does not undo.
- Rule against silently invented facts: placeholders or a „Założenia” section.
- GUI instructions section in `style.md` (bold UI labels, menu paths, Polish GUI verbs).
- Linter: `wsparcie` calque, capitalized reader pronouns mid-sentence („Twój”).
- Five instructional evals (2FA for customers, restic tutorial, mdadm disk replacement, English-only UI translation, internal onboarding).

### Changed
- How-to and tutorial templates use numbered step headings; how-to has an optional „Założenia” section; runbook has „Ograniczenia”.
- Workflow step 4 starts with a key-term consistency check.
- Developer-oriented evals 1–5 moved to `evals/regression-dev-docs.json`.

### Fixed
- Linter no longer flags protocol and version numbers (HTTP/1.1, „Wersja: 1.0”) as decimals.

## [0.4.0] – 2026-09-26

### Added
- `assets/templates/`: 14 fillable Polish templates – tutorial, how-to, concept, CLI/SQL/API reference, specification, README, ADR, changelog, runbook, postmortem, pull request, commit message.
- `scripts/lint_pl.py`: linter for dashes, quotes, Title Case headings, decimal and thousands separators, calques and jargon verbs in the public register; run by the skill workflow and in CI on the templates.

### Changed
- SKILL.md: content-type table links templates and states the register per type; workflow step 5 runs the linter.
- `content-types.md` holds rules per type; skeletons moved to templates.
- Phonetic polonizations (serwis, wolumin) and coined verbs (wyewikować, scordonować, scache'ować) replaced and listed under forms to avoid.

## [0.3.0] – 2026-09-26

### Added
- `polish-technical-vocabulary.md`: register model (publiczna / wewnętrzna / rozmowa), spelling rules for jargonized verbs (z-/s-/ze-/za- prefixes, apostrophes), inflection of English nouns, verb tables per domain, forms to avoid.
- Evals for internal (runbook) and public registers.

### Changed
- Em dash (U+2014) forbidden; en dash (U+2013) is the only dash. Enforced by `scripts/validate_skills.py`.
- SKILL.md: choose register before writing; description covers runbooks, postmortems and PR descriptions.

## [0.2.0] – 2026-09-26

### Added
- Content-type templates (tutorial, how-to, concept, CLI/SQL/API reference, specification) modelled on Kubernetes, PostgreSQL, MDN and RFC structures.
- `style.md`: anti-calque catalogue and phrasebook drawn from published Polish docs.
- `requirements-language.md`: Polish mapping of RFC 2119/8174 requirement keywords.
- Expanded terminology (Git, Kubernetes, administration, databases, doc vocabulary).
- Evals for reference pages, specifications and translation.

### Changed
- `document-types.md` replaced by `content-types.md`.
- Register guidance: address the reader as "ty", gender-neutral phrasing.

## [0.1.0] – 2026-09-26

### Added
- Initial scaffold of the `writing-docs-in-polish` skill.
