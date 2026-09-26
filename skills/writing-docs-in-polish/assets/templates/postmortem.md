<!-- Rejestr: inżynierska. Zasada „bez szukania winnych”: opisuj systemy i decyzje, nie osoby. Czas w formacie 24-godzinnym ze strefą (UTC lub CET/CEST). Szablon wyznacza strukturę, a nie limit treści: dodaj sekcję, gdy temat tego wymaga, i nie pomijaj istotnych informacji technicznych. -->
# Postmortem: <krótki opis incydentu>

- Data incydentu: <RRRR-MM-DD>
- Czas trwania: <od HH:MM do HH:MM strefa> (<N> min)
- Poziom: <SEV1 | SEV2 | SEV3>
- Autorzy: <osoby>
- Status: <szkic | przegląd | zamknięty>

## Podsumowanie

<2–3 zdania: co się stało, jaki był wpływ, jak to naprawiono.>

## Wpływ

- Użytkownicy: <liczba lub odsetek, funkcje, których dotyczyło>
- Dane: <czy doszło do utraty lub uszkodzenia danych>
- SLO: <zużyty budżet błędów>

## Oś czasu

| Czas (<strefa>) | Zdarzenie |
|---|---|
| <HH:MM> | <Deployment wersji X na produkcję.> |
| <HH:MM> | <Alert `<nazwa_alertu>`.> |
| <HH:MM> | <Rollback, usługa wraca do normy.> |

## Przyczyna źródłowa

<Techniczna przyczyna (root cause). Jeśli jest ich kilka, wymień wszystkie.>

## Czynniki sprzyjające

- <Np. brak testu, który wykryłby regresję.>

## Wykrycie i reakcja

<Jak wykryto problem i ile to trwało. Co przyspieszyło lub spowolniło reakcję.>

## Co poszło dobrze

## Co poszło źle

## Gdzie mieliśmy szczęście

## Działania naprawcze

| Działanie | Typ | Właściciel | Termin | Zgłoszenie |
|---|---|---|---|---|
| <Dodać alert na …> | zapobieganie | <osoba> | <RRRR-MM-DD> | <link> |

## Wnioski
