# Requirement keywords (RFC 2119 / RFC 8174 in Polish)

Use in specifications, API contracts and compliance docs. Per RFC 8174, keywords carry normative meaning only in UPPERCASE; lowercase "musi" or "powinien" is ordinary prose.

## Mapping

| RFC 2119 | Polish | Meaning |
|---|---|---|
| MUST, REQUIRED, SHALL | MUSI, WYMAGANE | Absolute requirement |
| MUST NOT, SHALL NOT | NIE MOŻE | Absolute prohibition |
| SHOULD, RECOMMENDED | POWINIEN, ZALECANE | Required unless there is a valid, understood reason not to |
| SHOULD NOT, NOT RECOMMENDED | NIE POWINIEN, NIEZALECANE | Forbidden unless there is a valid, understood reason |
| MAY, OPTIONAL | MOŻE, OPCJONALNE | Truly optional |

Inflect the keyword to agree with the subject and keep it uppercase: POWINIEN / POWINNA / POWINNO / POWINNY; MUSI / MUSZĄ; MOŻE / MOGĄ; NIE MOŻE / NIE MOGĄ.

## Declaration (put in "Konwencje i terminologia")

```markdown
Słowa kluczowe „MUSI” (ang. MUST), „NIE MOŻE” (MUST NOT), „WYMAGANE” (REQUIRED),
„POWINIEN” (SHOULD), „NIE POWINIEN” (SHOULD NOT), „ZALECANE” (RECOMMENDED),
„NIEZALECANE” (NOT RECOMMENDED), „MOŻE” (MAY) i „OPCJONALNE” (OPTIONAL)
w tym dokumencie należy interpretować zgodnie z BCP 14 [RFC2119] [RFC8174]
wyłącznie wtedy, gdy są zapisane wielkimi literami, jak w tym akapicie.
```

## Rules
- One requirement per sentence, so each can be tested and referenced.
- The subject is the implementing party: "Klient MUSI…", "Serwer NIE MOŻE…".
- Avoid lowercase "musi/powinien" near normative text; use "należy się spodziewać", "zwykle" etc. for non-normative prose so readers do not confuse the two.
- Never write "NIE MUSI" – it is not a keyword; use "MOŻE" (optional) instead.
