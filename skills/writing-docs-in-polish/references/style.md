# Style: natural Polish technical prose

## Contents
- Anti-calque catalogue (wrong → right)
- Sentence-level patterns
- Phonetic polonizations
- GUI instructions
- Phrasebook: recurring documentation phrases
- Consistency traps

These rules apply to every register except jargon, which inżynierska and potoczna docs may use (see polish-technical-vocabulary.md). The "wrong" forms below were observed in real published Polish translations of major projects. They are understandable but mark text as translated.

## Anti-calque catalogue

| Avoid | Write | Why |
|---|---|---|
| Kubernetes posiada ekosystem | Kubernetes ma ekosystem | "posiadać" = legal ownership; for features use "mieć", "zawierać" |
| obrazy nie wspierają Secure Boot | obrazy nie obsługują Secure Boot | "wspierać" = moral/financial support; software "obsługuje" |
| dedykowany serwer | osobny / przeznaczony do … serwer | "dedykować" = dedicate a book |
| w oparciu o konfigurację | na podstawie konfiguracji | |
| bazuje na Debianie | opiera się na Debianie / jest oparty na Debianie | |
| adresować problem | rozwiązywać problem | |
| aplikować zmiany | wprowadzać / stosować zmiany | |
| przy pomocy narzędzia | za pomocą narzędzia | "przy pomocy" = with a person's help |
| kliknij na przycisk | kliknij przycisk | |
| Dla dokładniejszych instrukcji, zobacz … | Dokładniejsze instrukcje znajdziesz w … | English fronted adverbial |
| odwołaj się do artykułu | zajrzyj do artykułu / zobacz artykuł | "refer to" |
| Ten rozdział dokonuje przeglądu … | W tym rozdziale omówiono … | Inanimate subject doing a mental action |
| Ta funkcja pozwala ci na … | Funkcja umożliwia … / Dzięki funkcji możesz … | |
| mógłbyś chcieć wykonać … | możesz wykonać … | Stacked English modals |
| bardzo-wysokiego-poziomu, znajdź-i-zamień | bardzo wysokiego poziomu, „znajdź i zamień” | English hyphenated compounds |
| samo-naprawianie, wysoko-poziomowy | samonaprawianie, wysokopoziomowy | Polish prefixes and compounds are written jointly |
| pomiędzy Archem, a innymi | między Archem a innymi | No comma in "między X a Y" |
| twój plik README jest śledzony | plik README jest śledzony | Drop English possessives where obvious |
| jest wykonywane przez serwer | serwer wykonuje | Passive overuse |
| w celu uruchomienia aplikacji należy … | aby uruchomić aplikację, … | Nominal style |
| restartuje | uruchamia ponownie | "restartować" acceptable informally, not in formal docs |
| na końcu dnia, w tym momencie (at this point) | ostatecznie, teraz / na tym etapie | Idiom calques |
| Instalacja i Usuwanie Pakietów | Instalacja i usuwanie pakietów | Title Case |

## Sentence-level patterns

- **Put the goal first:** "Aby utworzyć bazę, uruchom:" – not "Uruchom poniższe, aby utworzyć bazę:" when the goal matters more.
- **Condition before action:** "Jeśli polecenie zakończy się błędem, sprawdź …".
- **One idea per sentence** in procedures; longer sentences are fine in concept pages.
- **Vary the verb, keep the term:** synonyms for actions are fine, synonyms for defined terms are not.
- **Numbers inflect the noun:** 1 plik, 2–4 pliki, 5+ plików, 22 pliki, 25 plików.
- **Inflect English terms by Polish rules**, add endings without an apostrophe unless the word ends in a silent letter: commit → commita, pod → poda, deployment → deploymentu, cache → cache'u, Kubernetes → Kubernetesa, Git → Gita (Pro Git uses both "Git" and "Gita" – pick "Gita" consistently).
- **Acronyms inflect with a hyphen:** API (nieodmienne), URL → URL-a, SDK (nieodmienne), PR → PR-a.

## Phrasebook

| Situation | Phrase |
|---|---|
| Introduce a command | "Aby …, uruchom:" / "Uruchom polecenie:" |
| Show expected output | "Wynik powinien wyglądać podobnie do poniższego:" |
| Prerequisites | "Zanim zaczniesz" / "Wymagania wstępne" |
| Further reading | "Więcej informacji znajdziesz w …" |
| Next steps | "Co dalej" |
| Optional step | "(opcjonalnie)" at the start of the step heading or sentence |
| Replace placeholder | "Zastąp `<nazwa>` nazwą …" |
| Wait for state | "Może minąć kilka sekund, zanim … Jeśli widzisz …, spróbuj ponownie." |
| Default value | "Domyślnie: `…`." / "Wartość domyślna to `…`." |
| Page scope | "Na tej stronie znajdziesz …" / "Ten przewodnik opisuje …" |
| Assumed knowledge | "Zakładamy, że znasz …" |
| English-only link | "… (w języku angielskim)" |
| Gloss English output | „Changes to be committed” (zmiany do zatwierdzenia) |

## Phonetic polonizations

Words that respell an English term in Polish spelling ("serwis" for *service*, "wolumin" for *volume*) are neither Polish nor the recognizable English term. "Serwis" stays correct in its own senses: maintenance („okno serwisowe”, „serwis techniczny”) and websites („serwis internetowy”). Use a genuine Polish word (usługa) or keep the English term and inflect it (Service, volume'u). Words fully established in Polish dictionaries are fine: kontener, klaster, serwer, commit, tag.

## GUI instructions

- UI element names in **bold**, exactly as displayed. If the UI is in Polish, use its Polish labels; if it is English-only, keep the English label and gloss once: kliknij **Settings** (Ustawienia).
- Menu paths: **Ustawienia** > **Konto** > **Bezpieczeństwo** – one separator style per document.
- Say where before what: "W prawym górnym rogu kliknij **Zapisz**."
- Keys and shortcuts: `Ctrl+C`, `Enter`, `Cmd+Shift+4`.

| English | Polish |
|---|---|
| click / double-click / right-click | kliknij / kliknij dwukrotnie / kliknij prawym przyciskiem myszy |
| select (from a list) | wybierz |
| check / clear a checkbox | zaznacz / wyczyść pole wyboru |
| turn on / off (toggle) | włącz / wyłącz przełącznik |
| enter, type | wpisz, wprowadź |
| tap / swipe (mobile) | naciśnij / przesuń palcem |
| drag | przeciągnij |
| button / field / tab / drop-down | przycisk / pole / karta / lista rozwijana |
| dialog box / window | okno dialogowe / okno |
| sign in / sign out | zaloguj się / wyloguj się |
| scan the QR code | zeskanuj kod QR |

## Consistency traps
Pick one and hold it for the whole document set:
- polecenie (not komenda) for commands
- katalog (developer docs) vs folder (end-user GUI docs)
- usługa vs Service – "usługa" in general prose; "Service" when it is a Kubernetes object kind; not "serwis" for service (fine for maintenance and websites)
- Pod vs pod – Kubernetes PL mixes both; use lowercase "pod" in prose, `Pod` in code
- plik konfiguracyjny vs konfig – never "konfig" in docs
- logi vs dzienniki – "logi" is accepted in developer docs; "dziennik systemowy" for journald/syslog
