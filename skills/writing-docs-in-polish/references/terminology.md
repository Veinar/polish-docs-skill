# IT terminology (EN → PL)

"Keep" = the English term is standard in Polish IT; keep it and inflect by Polish rules. Where sources differ, the first form is the default; follow an existing project glossary if there is one.

## Contents
- Decision tree: service and similar ambiguous terms
- General software and development
- Version control (Git)
- Containers and Kubernetes
- Operating systems and administration
- Databases
- Documentation vocabulary

## Decision tree: service and similar ambiguous terms

1. Is it an identifier (Kubernetes `Service`, a systemd unit, an API object, a config key)? Keep it exactly: `Service`, `nginx.service`.
2. Is it a microservice? "mikroserwis" is established Polish; use it or "usługa", consistently.
3. Otherwise "usługa" (publiczna) or "usługa" / English "service" inflected ("service'u") in inżynierska and potoczna, one form per document.
4. "serwis" only in its own senses: maintenance or repair ("okno serwisowe", "serwis techniczny") and websites ("serwis internetowy").
5. A term the user or the project already uses wins over all of the above.

## General software and development

| English | Polish | Notes |
|---|---|---|
| feature | funkcja | "funkcjonalność" only for a set of functions |
| support (a feature) | obsługiwać | never "wspierać" |
| dependency | zależność | |
| library / framework | biblioteka / framework | framework: keep |
| build (noun) | kompilacja, build | "zbudować" for the verb |
| release | wydanie | |
| deploy / deployment | wdrożyć / wdrożenie | |
| rollback | wycofanie zmian | |
| request / response | żądanie / odpowiedź | "zapytanie" for queries |
| endpoint | punkt końcowy, endpoint | endpoint is common in API docs |
| callback | wywołanie zwrotne | |
| thread / process | wątek / proces | |
| cache | pamięć podręczna; cache (keep, "cache'u") | |
| environment variable | zmienna środowiskowa | |
| command line / shell | wiersz poleceń / powłoka | |
| prompt (shell) | znak zachęty | |
| flag / option | flaga / opcja | |
| placeholder | symbol zastępczy | |
| deprecated | przestarzały, wycofywany | |
| breaking change | zmiana niekompatybilna wstecz | |
| backward compatible | zgodny wstecz | |
| troubleshooting | rozwiązywanie problemów | |
| prerequisites | wymagania wstępne | |
| getting started | pierwsze kroki | |
| tutorial | samouczek | "tutorial" acceptable |
| how-to guide | instrukcja, przewodnik | |
| embedding | osadzanie | not "embedowanie" |
| scheduling | planowanie, szeregowanie | |
| load balancing | równoważenie obciążenia | |
| high availability | wysoka dostępność | |
| secret (credentials) | dane poufne; Secret (Kubernetes kind) | |
| token | token | keep |
| sign in / sign out | zaloguj się / wyloguj się | |

## Version control (Git)
Pro Git PL translates most terms; developer docs usually keep them. Choose per audience and stay consistent.

| English | Developer docs | Pro Git PL |
|---|---|---|
| repository | repozytorium | repozytorium |
| commit (noun / verb) | commit / zatwierdzić (commitować) | zatwierdzenie / zatwierdzić |
| branch | gałąź | gałąź |
| merge | scalanie, merge | scalanie |
| rebase | rebase, zmiana bazy | zmiana bazy |
| staging area / index | poczekalnia (staging area) | przechowalnia, poczekalnia |
| snapshot | migawka | migawka |
| stash | schowek, stash | schowek |
| submodule | moduł zależny, submoduł | moduł zależny |
| working directory | katalog roboczy | katalog roboczy |
| pull request | pull request (PR) | – |
| tag | tag, znacznik | tagowanie |
| hook | hook, skrypt zaczepienia | – |

## Containers and Kubernetes
From the Kubernetes Polish localization glossary. API object kinds stay English and inflect.

| English | Polish |
|---|---|
| container | kontener |
| container image | obraz kontenera |
| cluster | klaster |
| node / worker node | węzeł / węzeł roboczy |
| control plane | warstwa sterowania |
| Pod | Pod (prose: pod, poda, pody) |
| Deployment | Deployment (deploymentu) |
| Service | `Service` (object kind); usługa (general prose), never „serwis” |
| namespace | przestrzeń nazw |
| volume | volume (inflected: volume'u) |
| workload | obciążenie, workload |
| rolling update | aktualizacja krocząca |
| staged / phased rollout | wdrożenie etapowe |
| horizontal scaling | skalowanie horyzontalne / poziome |
| self-healing | samonaprawianie |
| desired state | stan oczekiwany |

## Operating systems and administration

| English | Polish |
|---|---|
| boot / bootloader | rozruch / program rozruchowy |
| Secure Boot | bezpieczny rozruch (Secure Boot) |
| mirror | serwer lustrzany |
| package source vs source package | źródło pakietów vs pakiet źródłowy |
| partitioning | partycjonowanie |
| mount | montować |
| live environment | środowisko live |
| man page | strona podręcznika (man) |
| fingerprint (key) | odcisk palca klucza |
| upgrade (distribution) | aktualizacja do nowszego wydania |

## Databases

| English | Polish |
|---|---|
| database cluster (PostgreSQL) | klaster bazy danych |
| role / privilege | rola / uprawnienie |
| superuser | superużytkownik |
| table / view / index | tabela / widok / indeks |
| query / statement | zapytanie / instrukcja, polecenie SQL |
| transaction / commit / rollback | transakcja / zatwierdzenie / wycofanie |
| replication / replica | replikacja / replika |
| write-ahead log | dziennik zapisu z wyprzedzeniem (WAL) |

## Documentation vocabulary

| English | Polish |
|---|---|
| Synopsis | Składnia |
| Description / Options / Parameters | Opis / Opcje / Parametry |
| Return value / Exceptions | Wartość zwracana / Wyjątki |
| Exit status | Kod zakończenia |
| Examples / Notes / See also | Przykłady / Uwagi / Zobacz też |
| Compatibility | Zgodność |
| Security considerations | Względy bezpieczeństwa |
| Normative / Informative references | Źródła normatywne / informacyjne |
| Abstract | Streszczenie |
| Note / Tip / Caution / Warning | Informacja / Wskazówka / Uwaga / Ostrzeżenie |
| Clean up | Sprzątanie |
| What's next | Co dalej |
