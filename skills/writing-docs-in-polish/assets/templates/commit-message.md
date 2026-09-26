<!-- Rejestr: potoczna. Conventional Commits: typ i zakres po angielsku (parsują je narzędzia), opis po polsku w trybie rozkazującym, małą literą, bez kropki, do 72 znaków w pierwszym wierszu. Treść wyjaśnia „dlaczego”, nie „co”. Stopki czytane przez narzędzia (BREAKING CHANGE, Refs) zostają po angielsku. Szablon wyznacza strukturę, a nie limit treści: dodaj sekcję, gdy temat tego wymaga, i nie pomijaj istotnych informacji technicznych. -->
<typ>(<zakres>): <opis w trybie rozkazującym>

<Dlaczego ta zmiana jest potrzebna i jaki problem rozwiązuje.
Zawijaj wiersze na 72 znakach.>

<Opcjonalnie: istotne szczegóły implementacji lub ograniczenia.>

Refs: #<numer>
BREAKING CHANGE: <co przestaje działać i jak migrować>

<!--
Przykład:

fix(api): popraw paginację listy zamówień

Przy ostatniej stronie endpoint zwracał pusty kursor zamiast null,
przez co klient mobilny zapętlał pobieranie.

Refs: #482
-->
