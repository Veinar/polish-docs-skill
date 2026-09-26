# Polish typography for technical docs

## Contents
- Quotation marks
- Dashes and hyphens
- Numbers and units
- Dates and times
- Headings and numbering
- Abbreviations
- Lists and punctuation
- Single-letter words at line ends

## Quotation marks
- Primary: „cudzysłów” (U+201E opening, U+201D closing).
- Nested: «wewnętrzny» or ‚wewnętrzny’.
- Code, literal values and UI strings copied verbatim go in backticks, not quotes.

## Dashes and hyphens
- Hyphen `-` only inside compounds of equal parts: "biało-czerwony", "klient-serwer". Prefixes join without a hyphen: "samonaprawianie", "wielowątkowy", "nadrzędny".
- Sentence dash (myślnik): spaced en dash ` – ` (U+2013). **Never use the em dash (U+2014)** – not in prose, headings, lists, tables or code comments, even where a source text uses it. When translating, replace every em dash with a spaced en dash.
- Ranges: en dash without spaces: 10–20, 2024–2026.
- Never a hyphen surrounded by spaces (" - ") as a dash.

## Numbers and units
- Decimal comma: 0,5 s; 3,14.
- Thousands: space (preferably non-breaking) for numbers ≥ 10 000; four-digit numbers stay together: 1000, 10 000.
- Space between value and unit: 512 MiB, 30 s, 100 %. Exception: degrees ° stuck to the number in angles.
- Binary vs decimal units: MiB/GiB for memory and disk sizes computed in powers of 2, MB/GB otherwise – follow what the software reports.
- Version numbers and code values keep their original form: `v1.2.3`, `0.5` in a config file.

## Dates and times
- Prose: "26 września 2026 r." (genitive month, lowercase).
- Tables/changelogs: ISO 8601 `2026-09-26`.
- Time: 24-hour format, "14:30".

## Headings and numbering
- Sentence case, no final full stop.
- Multi-level numbering: "4.1. Metody instalacji" (full stop after the number) or "4.1 Metody instalacji" – one style per document.

## Abbreviations
With full stop: np., m.in., tzn., tj., itd., itp., ok., r. (rok), w. (wiek), nr.
Without full stop when the abbreviation ends with the last letter of the word: dr, mgr, nr (numer).

## Lists and punctuation
- Items that complete a lead-in sentence: start lowercase, end with a comma or semicolon, last with a full stop.
- Items that are full sentences: start uppercase, end with a full stop.
- Items that are short labels/fragments: no final punctuation – be consistent within one list.
- Comma before "że", "który", "aby", "ponieważ", "jeśli", "gdy" (subordinate clauses).
- No Oxford comma: "A, B i C".

## Single-letter words at line ends
Polish typesetting avoids single-letter words (a, i, o, u, w, z) at the end of a line. In Markdown do NOT insert non-breaking spaces by default – they are invisible, break search and diffs. Apply only when the output is typeset (PDF, print, HTML with explicit `&nbsp;`) and the user asks for it.
