# Translation and proofreading

The source is authoritative. Keep every fact, prerequisite, warning, limit, example, version constraint, ordering dependency, negation and caveat, and keep command and API semantics exact. Never shorten a technical source to make the Polish tidier. Proofreading changes the language, not the content: no step, value or warning added or removed.

- Translate all prose; no English paragraphs left behind.
- Identifiers, commands, flags and output stay verbatim. Gloss an English-only UI label once: **Settings** (Ustawienia). Quote English output and gloss it once: „Running” (działa).
- Localize numbers (2,5 GB; 1000 or 1 000), turn em dashes into en dashes and straight quotes into „…”.
- If the source contradicts itself, keep both versions and tell the user in your reply; do not fix it.
- Note the source version when known. Mark links to English-only pages "(w języku angielskim)".
- The output is the translation only: no copy of the source, no notes.

## Negations and limits

Losing a negation is the worst translation error: the Polish reads well and says the opposite. Check each of these words in the source against the translation.

| English | Polish |
|---|---|
| does not / cannot | nie / nie można |
| must not | nie wolno / NIE MOŻE (in a specification) |
| unless | chyba że / o ile nie |
| only | tylko / wyłącznie |
| except | z wyjątkiem |
| not supported | nie jest obsługiwane |
| does not affect / does not revert | nie wpływa na / nie cofa |


"This command does not restore database migrations." becomes „To polecenie nie przywraca migracji bazy danych.” Never soften it to „ogranicza się do…”.
