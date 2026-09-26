# Content types: rules per type

Pick one type per page. Fillable skeletons live in `assets/templates/` (listed in SKILL.md); this file holds the shared elements and the rules that make each type work. Drop template sections that would be empty; do not invent content to fill them.

## Contents
- Shared elements (conventions, admonitions, version markers, cross-references)
- Rules per content type

## Shared elements

### Conventions section
Larger document sets (books, manuals) open with a "Konwencje" section, as PostgreSQL and ArchWiki do:

```markdown
## Konwencje

W opisie składni poleceń:
- nawiasy kwadratowe `[` `]` oznaczają elementy opcjonalne,
- nawiasy klamrowe `{` `}` z kreską pionową `|` oznaczają wybór jednej z możliwości,
- wielokropek `...` oznacza, że poprzedni element można powtórzyć.

Polecenia powłoki poprzedza znak zachęty `$` (zwykły użytkownik) lub `#` (root), a polecenia SQL – znak `=>`.
Tekst w nawiasach ostrych, np. `<nazwa_bazy>`, zastąp własną wartością.
```

### Admonitions
Use a small fixed set, always with the same labels:

| Label | Use for |
|---|---|
| **Informacja** | Useful context that does not change the procedure |
| **Wskazówka** | Shortcut or better way to do something |
| **Uwaga** | Something that may surprise or cause minor problems |
| **Ostrzeżenie** | Risk of data loss, security issue or outage |
| **Pojęcie** | Short definition that disambiguates a term (Debian Handbook's "SŁOWNICZEK" boxes, e.g. *pakiet źródłowy* vs *źródło pakietów*) |
| **Podstawy** | Background for beginners that experts can skip ("WRACAJĄC DO PODSTAW") |

Markdown form: `> **Ostrzeżenie:** treść.` – or the platform's native syntax (`> [!WARNING]`, `:::warning`, `.. warning::`) with the Polish label as the title if the renderer shows English by default.

### Version markers (reference docs)
- "Dodano w wersji 2.3."
- "Zmieniono w wersji 3.0: parametr `timeout` przyjmuje wartość w sekundach."
- "Przestarzałe od wersji 3.2, zostanie usunięte w wersji 4.0. Zamiast tego użyj `connect()`."

### Cross-references
End pages with "Zobacz też" (reference) or "Co dalej" (tutorial, task). Order: related pages of the same kind first, then other docs, then external sources (PostgreSQL's rule). Link text describes the target – never "kliknij tutaj".

## Rules per content type

**Tutorial** (`tutorial.md`, publiczna). Teaches by doing a complete, working example; every step must succeed. Minimal theory, link to concept pages. Steps are numbered headings ("## 1. Utwórz projekt"). Show expected output after each command. End with "Sprzątanie" and "Co dalej".

**How-to** (`how-to.md`). Solves one concrete problem for a reader who knows the basics. Title is a verbal noun naming the goal ("Konfigurowanie TLS…"); steps are numbered ("## 1. Utwórz przestrzeń nazw" for long steps, a numbered list for short ones) and start with an imperative. Always include "Weryfikacja"; add "Rozwiązywanie problemów" in the Objaw → Przyczyna → Rozwiązanie form.

**Concept** (`concept.md`, publiczna). Explains how and why; no procedures. Order: problem, mechanism, consequences (Pro Git chapter 1, Kubernetes "Przegląd"). Define each term on first use; use a **Pojęcie** box to separate easily confused terms.

**CLI reference / man page** (`reference-cli.md`, publiczna). PostgreSQL / man-page section order; omit sections that do not apply. Option descriptions start with a 3rd-person verb ("Wyświetla…", "Określa…") and state the default. "Kod zakończenia" only when non-zero codes differ in meaning; "Diagnostyka" only for unusual messages.

**SQL reference** (`reference-sql.md`, publiczna). PostgreSQL order: Składnia, Opis, Parametry, Wynik, Uwagi, Przykłady, Zgodność, Zobacz też. SQL keywords stay uppercase English: "klauzula `WHERE`".

**API reference** (`reference-api.md`, publiczna). MDN order: Składnia, Parametry, Wartość zwracana, Wyjątki, Opis, Przykłady, Zgodność, Zobacz też. First sentence in 3rd person ("Zwraca…").

**Specification** (`specification.md`, publiczna). RFC structure and requirement keywords (requirements-language.md). "Względy bezpieczeństwa" is mandatory: if there are no risks, say so and why. Cover the threats typical for the mechanism, e.g. for signed messages: replay (timestamp, nonce), key rotation, constant-time comparison. Expand abbreviations on first use, define terms once, avoid double negatives, one requirement per sentence (RFC 7322).

**README** (`readme.md`). One or two sentences on what and for whom, then the shortest path to a working result.

**ADR** (`adr.md`, wewnętrzna). Title states the decision as a sentence. List positive, negative and neutral consequences.

**Changelog** (`changelog.md`, publiczna). Keep a Changelog with Polish section names. Start entries consistently with a past impersonal verb ("Dodano…") or a noun; mark breaking changes with **Zmiana niekompatybilna wstecz:**.

**Runbook** (`runbook.md`, wewnętrzna). Written for someone paged at 3 a.m.: short sentences, copy-pasteable commands, branching diagnosis ("Jeśli…, przejdź do kroku N"), explicit escalation criteria with a time limit. Say what the fix does not undo (e.g. `kubectl rollout undo` does not revert ConfigMap/Secret changes or database migrations). Team jargon is expected.

**Postmortem** (`postmortem.md`, wewnętrzna). Blameless: describe systems and decisions, not people. Timeline in 24-hour time with an explicit time zone. Every corrective action has an owner, a deadline and a ticket.

**Pull request** (`pull-request.md`, wewnętrzna). Why before what; how to test; risk and how to roll back.

**Commit message** (`commit-message.md`, wewnętrzna). Conventional Commits: type and scope stay English (tools parse them), the description is Polish, imperative, lowercase, no final full stop, subject line up to 72 characters. The body explains why. Tool-parsed footers (`BREAKING CHANGE:`, `Refs:`) stay English.
