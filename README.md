# writing-docs-in-polish

![GitHub License](https://img.shields.io/github/license/Veinar/polish-docs-skill?color=blue)

Skill dla Claude, który pisze, tłumaczy i poprawia dokumentację techniczną po polsku: naturalnym językiem, z polską typografią i spójną terminologią, na poziomie dokumentacji Kubernetesa, Pro Git czy PostgreSQL.

## Dla kogo jest ten skill

- **Autorzy i opiekunowie projektów**, którzy piszą README, instrukcje, dokumentację API i dziennik zmian po polsku.
- **Zespoły DevOps i SRE**, którym potrzebne są runbooki, postmortemy, ADR-y i opisy PR-ów w języku, jakim naprawdę pracuje zespół.
- **Tłumacze i redaktorzy techniczni**, którzy tłumaczą dokumentację z angielskiego albo poprawiają istniejące teksty bez gubienia treści.
- **Firmy z dokumentacją dla polskich klientów**, którym zależy na jednym słownictwie w całej dokumentacji.

Skill nie zastępuje przeglądu przez osobę, która zna projekt i jego terminologię. Przyspiesza pisanie i pilnuje reguł, o których łatwo zapomnieć.

## Co potrafi

- Pisze dokumenty według gotowych szablonów: samouczki, instrukcje, opisy koncepcji, dokumentację poleceń CLI, SQL i API, specyfikacje, README, ADR-y, runbooki, postmortemy, dziennik zmian, opisy PR-ów i komunikaty commitów.
- Tłumaczy i poprawia teksty, zachowując każdą negację, ostrzeżenie, limit i wartość ze źródła. Nie dopisuje faktów, których nie podałeś.
- Dobiera rejestr języka do odbiorcy: dokumentacja publiczna używa polskich czasowników (wdrożyć, zbudować), dokumentacja zespołowa naturalnego żargonu (`zdeployuj`, `zrollbackuj`).
- Dopasowuje się do projektu: wykrywa język istniejących dokumentów, styl nazw plików oraz zapis identyfikatorów i symboli zastępczych (snake_case, camelCase, kebab-case, PascalCase) i nie narzuca własnego.
- Pilnuje typografii: półpauza zamiast pauzy, cudzysłowy „…”, przecinek dziesiętny, nagłówki z małej litery.
- Sprawdza gotowy tekst wbudowanym linterem i poprawia mechaniczne błędy automatycznie.

## Wymagania

- Claude Code albo Claude.ai z obsługą skilli.
- Python 3 do skryptów pomocniczych. Używają tylko biblioteki standardowej, testowano na wersji 3.12.

## Instalacja

### Claude Code: plugin z GitHuba

1. Dodaj repozytorium jako marketplace:

   ```bash
   claude plugin marketplace add Veinar/polish-docs-skill
   ```

2. Zainstaluj plugin:

   ```bash
   claude plugin install writing-docs-in-polish@veinar-skills
   ```

   Wynik kończy się wierszem „Successfully installed plugin” (zainstalowano plugin).

3. Sprawdź, czy plugin działa:

   ```bash
   claude plugin list
   ```

   Przy `writing-docs-in-polish@veinar-skills` powinien być status `enabled`.

4. Uruchom nową sesję (`claude`) albo wpisz `/reload-plugins` w trwającej.

### Claude Code: lokalnie z klonu

Sklonuj repozytorium, dodaj marketplace ze ścieżki i zainstaluj plugin tak samo jak wyżej:

```bash
git clone https://github.com/Veinar/polish-docs-skill.git
claude plugin marketplace add <sciezka_do_repozytorium>
claude plugin install writing-docs-in-polish@veinar-skills
```

Zmiany w plikach skilla wczytasz poleceniem `/reload-plugins`. Plugin możesz wyłączyć poleceniem `claude plugin disable writing-docs-in-polish@veinar-skills`, a włączyć ponownie przez `claude plugin enable`.

### Claude Code: ręczne kopiowanie

Skopiuj katalog skilla do katalogu skilli Claude Code:

```bash
cp -r skills/writing-docs-in-polish ~/.claude/skills/
```

Ten wariant działa we wszystkich projektach. Aby użyć skilla tylko w jednym projekcie, skopiuj go do `<katalog_projektu>/.claude/skills/`. Skill wczyta się przy następnej sesji.

### Claude.ai

Spakuj katalog `skills/writing-docs-in-polish` do pliku ZIP i wgraj go w ustawieniach Claude.ai, w sekcji poświęconej skillom (Skills).

## Jak używać

Nie musisz niczego włączać. Skill uruchamia się sam, gdy prosisz o dokumentację po polsku, o tłumaczenie dokumentacji na polski albo o poprawę polskiego tekstu technicznego. Do dużych zadań podaj repozytorium, żeby skill mógł dopasować się do jego konwencji.

### Przykładowe polecenia

```
Napisz README po polsku dla biblioteki kolejka-zadan. Instalacja przez pip, wymagany Python 3.11.
```

```
Przetłumacz na polski ten fragment dokumentacji API i zachowaj wszystkie ostrzeżenia: ...
```

```
Popraw językowo ten tekst. Nie zmieniaj treści technicznej i niczego nie skracaj: ...
```

```
Napisz runbook dla dyżurnych: rotacja certyfikatu TLS na serwerze nginx.
```

```
Napisz w katalogu docs/ stronę o poleceniu export, zgodną z konwencjami tego repozytorium.
```

Małe zadania (akapit, kilka wierszy) skill wykonuje bezpośrednio, bez szablonów. Przy dokumentach na stronę lub więcej przechodzi przez pełną procedurę: wybiera typ dokumentu i rejestr, sprawdza konwencje projektu, ustala zakres techniczny, pisze według szablonu, uzupełnia braki i uruchamia linter.

Odpowiedź zawiera sam dokument. Założenia i pytania otwarte skill zgłasza w osobnej wiadomości, a nie w tekście.

### Rejestry

Rejestr zależy od typu dokumentu. Możesz go też zmienić w poleceniu, na przykład: „napisz dla zespołu” albo „napisz dla klientów”.

| Rejestr | Dla kogo | Styl |
|---|---|---|
| `publiczna` | dokumentacja produktu, specyfikacje, czytelnicy zewnętrzni | polskie czasowniki: wdrożyć, zbudować, scalić; angielskie rzeczowniki odmienione (commita, poda) |
| `inżynierska` | runbooki, ADR-y, postmortemy, wewnętrzne README | żargon inżynierów: `zdeployuj`, `zrollbackuj`; bez slangu |
| `potoczna` | opisy PR-ów, komunikaty commitów, notatki | żargon i slang: `wywaliło się`, `odpal` |

### Typy dokumentów

| Typ | Szablon | Rejestr |
|---|---|---|
| samouczek | `tutorial` | publiczna |
| instrukcja | `how-to` | publiczna lub inżynierska |
| opis koncepcji | `concept` | publiczna |
| dokumentacja CLI, SQL, API | `reference-cli`, `reference-sql`, `reference-api` | publiczna |
| specyfikacja z MUSI, POWINIEN, MOŻE | `specification` | publiczna |
| README | `readme` | publiczna lub inżynierska |
| dziennik zmian | `changelog` | publiczna |
| ADR | `adr` | inżynierska |
| runbook | `runbook` | inżynierska |
| postmortem | `postmortem` | inżynierska |
| opis PR-a | `pull-request` | potoczna |
| komunikat commita | `commit-message` | potoczna |

Szablony leżą w `skills/writing-docs-in-polish/assets/templates/`.

### Narzędzia z linii poleceń

Skill korzysta ze skryptów, które możesz uruchamiać także samodzielnie. Poniższe polecenia wykonuj z katalogu głównego repozytorium.

**Linter.** Sprawdza półpauzy i cudzysłowy, nagłówki pisane wielkimi literami, kropki dziesiętne, kalki z angielskiego (`posiada`, `wspiera`, `w oparciu o`), niespójne symbole zastępcze oraz żargon i slang niepasujące do rejestru. Rejestr jest wymagany: podaj go w poleceniu albo w komentarzu `Rejestr:` w pliku.

```bash
python skills/writing-docs-in-polish/scripts/lint_pl.py --fix --register publiczna docs/
```

Opcja `--fix` sama poprawia półpauzy i cudzysłowy, a resztę wypisuje. Opcja `--strict` traktuje ostrzeżenia jak błędy, a `--placeholder-style camel` wymusza zapis symboli zastępczych (do wyboru: `snake`, `camel`, `kebab`, `pascal`).

**Słownik.** Wypisuje tylko pasujące wiersze glosariusza: odpowiedniki terminów, formy żargonowe dla każdego rejestru i kalki.

```bash
python skills/writing-docs-in-polish/scripts/term.py deploy rollback
```

**Konwencje projektu.** Wykrywa język istniejących dokumentów, styl nazw plików, zapis identyfikatorów i symboli zastępczych, cudzysłowy, myślniki, rejestr i pliki słownikowe.

```bash
python skills/writing-docs-in-polish/scripts/detect_conventions.py .
```

## Ograniczenia

- Skill obsługuje wyłącznie język polski. Instrukcje skilla są po angielsku, szablony i przykłady po polsku.
- Linter opiera się na heurystykach i bywa mylący, na przykład przy numerach wersji albo słowie `serwis` w znaczeniu konserwacji. Ostrzeżenia traktuj jako wskazówki.
- Model może się mylić w szczegółach narzędzi. Polecenia z wygenerowanej dokumentacji sprawdź przed publikacją.
- Terminy spoza słownika skill zostawia po angielsku i odmienia. Firmowe ustalenia zapisz w pliku słownika w repozytorium, a skill je zastosuje.

## Struktura repozytorium

```
.
├── .claude-plugin/           # manifest pluginu i marketplace
├── skills/
│   └── writing-docs-in-polish/
│       ├── SKILL.md          # główne instrukcje skilla
│       ├── references/       # dodatkowe reguły wczytywane w razie potrzeby
│       ├── assets/templates/ # 14 szablonów dokumentów
│       └── scripts/          # linter, słownik, wykrywanie konwencji
├── evals/                    # przypadki testowe skilla
├── scripts/                  # walidacja, testy i narzędzia do ewaluacji
└── .github/workflows/        # sprawdzenia uruchamiane w CI
```

## Rozwój i testy

Przed wysłaniem zmian uruchom z katalogu głównego:

```bash
python scripts/validate_skills.py
python -m unittest discover -s scripts
python skills/writing-docs-in-polish/scripts/lint_pl.py --strict --ignore placeholder-prose skills/writing-docs-in-polish/assets/templates
claude plugin validate .
```

Walidator pilnuje między innymi zgodności wersji w plikach i rozmiaru `SKILL.md`, który jest wczytywany przy każdym użyciu skilla.

Jakość skilla mierzy się na losowej próbce około 5 przypadków testowych, na najtańszym modelu, z porównaniem do odpowiedzi bez skilla. Procedura jest opisana w [evals/README.md](evals/README.md) (w języku angielskim).

## Współtworzenie

Propozycje terminów, poprawki i zgłoszenia błędów przekazuj jako issue lub pull request. Zmieniając reguły, dodaj test linta albo przypadek w `evals/`. We wszystkich plikach używaj półpauzy (–) i nigdy pauzy (znaku U+2014). Zasady pracy nad repozytorium opisuje plik [CLAUDE.md](CLAUDE.md) (w języku angielskim).

## Wersja i historia zmian

Aktualna wersja: 0.8.0. Historia zmian: [CHANGELOG.md](CHANGELOG.md) (w języku angielskim).

## Licencja

MIT © 2026 Veinar. Szczegóły w pliku [LICENSE](LICENSE).
