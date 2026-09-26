# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versioning follows [SemVer](https://semver.org/).

## [Unreleased]

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
