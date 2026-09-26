# Shared documentation elements

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
