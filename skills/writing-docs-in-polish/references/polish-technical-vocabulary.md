# Polish developer jargon: verbs, nouns and inflection

Polish engineers use Polish-inflected English terms ("zdeployuj na staging", "zrollbackuj deployment"). Replacing them with formal equivalents in internal docs sounds stiff; using them in public product docs sounds careless. Natural Polish is not formal Polish: the register decides.

## Contents
- Registers: when jargon is right
- Spelling rules for jargonized verbs
- Nouns kept in English, with inflection
- Verbs by domain
- Forms to avoid

## Registers: when jargon is right

| Register | Where | English nouns | Jargon verbs | Slang |
|---|---|---|---|---|
| **publiczna** | Product docs, man pages, specifications, tutorials for external users | Established ones, inflected (commit, pod, pipeline) | No: use Polish verbs (wdrożyć, zbudować, scalić, uruchomić ponownie) | No |
| **inżynierska** | Runbooks, ADRs, postmortems, onboarding, internal READMEs and how-tos | Freely | Yes (zdeployuj, zmerguj, zrollbackuj) | No |
| **potoczna** | PR descriptions, commit bodies, review comments, chat-like notes | Freely | Yes | Yes (marked *potoczna* in the tables below) |

Default when unclear: internal project docs → *inżynierska*; anything for customers or the open-source public → *publiczna*; PR and commit text → *potoczna*. Follow what the project's existing docs already do.

Within one document, stay in one register: don't mix "zdeployuj" and "wdróż" for the same action.

## Spelling rules for jargonized verbs

**Suffix:** English stem + `-ować`, conjugated like Polish verbs: deployować → deployuję, deployujesz, deployuj!, deployowany.

**Perfective prefix** (the finished action), chosen by pronunciation of the first sound:
- `z-` before vowels and voiced consonants: zdeployować, zbuildować, zmergować, zdebugować, zrefaktorować, zrollbackować
- `s-` before voiceless consonants (p, t, k, f, ch/h, c, s, sz, cz): spushować, spullować, spatchować, sprovisionować, sforkować, scherry-pickować
- `ze-` before s-, z- and hard clusters: zeskalować, zeskanować, zesquashować, zestubować
- `za-` in established forms: zacommitować, zaimplementować, zaaplikować, zamockować
- `prze-`, `wy-`, `o-` where Polish has a matching verb: przetestować, wypushować, otagować, wystawić

**Apostrophe** only when the English word ends in a silent letter: upgrade → upgrade'ować, merge → merge'a, cache → cache'ować, release → release'ować, image → image'u, override → override'ować, trace → trace'ować. No apostrophe otherwise: commita, builda, poda.

**Hyphenated English** keeps the hyphen: cherry-pickować, port-forwardować, rate-limitować.

## Nouns kept in English, with inflection

Keep these in English in every register (in *publiczna*, still prefer a Polish word when one is established, e.g. wdrożenie, gałąź, repozytorium – see terminology.md).

| Noun | D. (kogo/czego) | N. (kim/czym) | Pl. D. |
|---|---|---|---|
| deployment | deploymentu | deploymentem | deploymentów |
| build | builda / buildu | buildem | buildów |
| commit | commita | commitem | commitów |
| branch | brancha | branchem | branchy |
| merge | merge'a | merge'em | merge'y |
| rollback | rollbacku | rollbackiem | rollbacków |
| release | release'u | release'em | release'ów |
| pipeline | pipeline'u | pipeline'em | pipeline'ów |
| pod | poda | podem | podów |
| node | node'a | node'em | node'ów |
| namespace | namespace'u | namespace'em | namespace'ów |
| secret | secretu / secreta | secretem | secretów |
| image | image'u | image'em | image'ów |
| cache | cache'u | cache'em | – |
| endpoint | endpointu | endpointem | endpointów |
| request / response | requestu / response'u | requestem / response'em | requestów |
| job / runner | joba / runnera | jobem / runnerem | jobów / runnerów |
| bug / issue | buga / issue | bugiem / issue | bugów / issues |
| hotfix / patch | hotfixa / patcha | hotfixem / patchem | hotfixów / patchy |
| incident | incydentu | incydentem | incydentów (Polish word) |

Also kept as-is: workflow, payload, header, token, config, manifest, registry, repo, artifact/artefakt, proxy, gateway, load balancer, ingress, backend, frontend, worker, daemon, operator, controller, trace, span, log(i), alert, feature, root cause.

## Verbs by domain

Columns: **publiczna** form | **inżynierska** jargon (natural in writing). Slang forms are marked *(potoczna)* and belong only in the potoczna register.

### Git and code

| English | Publiczna | Wewnętrzna | Notes |
|---|---|---|---|
| commit | zatwierdzić | zacommitować | |
| push / pull | wypchnąć / pobrać | wypushować, spushować / spullować | |
| merge | scalić | zmergować | |
| rebase | zmienić bazę | zrebase'ować | |
| cherry-pick | przenieść commit | scherry-pickować | "zrobić cherry-picka" also natural |
| squash | połączyć commity | zesquashować | |
| stash | odłożyć zmiany | zrobić stash | verb form "zestashować" is rare |
| checkout | przełączyć się na gałąź | przełączyć się na brancha | avoid "zcheckoutować" in writing |
| fork / clone | utworzyć fork / sklonować | sforkować / sklonować | |
| tag / release | oznaczyć tagiem / wydać | otagować / wypuścić, zrelease'ować | |
| refactor | przebudować, zrefaktoryzować | zrefaktorować | |
| debug | debugować | zdebugować | |
| mock / stub | zasymulować | zamockować / zestubować | |
| override | nadpisać | nadpisać | "zoverride'ować" only in chat |
| validate / sanitize | zweryfikować, zwalidować / oczyścić | zwalidować / zsanityzować | |
| serialize / parse | serializować / analizować składniowo | zserializować / sparsować | "sparsować" acceptable in any dev register |
| deprecate | oznaczyć jako przestarzałe | zdeprecjonować | |
| benchmark / profile | zmierzyć wydajność / profilować | zbenchmarkować / sprofilować | |

### Build, CI/CD, releases

| English | Publiczna | Wewnętrzna |
|---|---|---|
| build | zbudować | zbuildować |
| test | przetestować | przetestować |
| deploy | wdrożyć | zdeployować |
| rollback | wycofać | zrollbackować, zrobić rollback |
| trigger (pipeline) | uruchomić | striggerować, odpalić *(potoczna)* |
| run / rerun | uruchomić / uruchomić ponownie | uruchomić / uruchomić ponownie, puścić ponownie *(potoczna)* |
| retry | ponowić | ponowić, zretryować |
| fail | zakończyć się błędem | sfailować, wywalić się *(potoczna)* |
| promote | przenieść na (środowisko) | wypromować |
| approve | zatwierdzić | zaakceptować, zaapprove'ować |
| cache | buforować | wrzucić do cache'u |
| publish | opublikować | opublikować |

### Kubernetes and infrastructure

| English | Publiczna | Wewnętrzna |
|---|---|---|
| restart | uruchomić ponownie | zrestartować |
| scale | przeskalować | zeskalować, przeskalować |
| apply | zastosować (manifest) | zaaplikować |
| expose | udostępnić | wystawić |
| drain / cordon | opróżnić / wyłączyć z harmonogramowania | zdrainować / zrobić cordon |
| taint / label / annotate | dodać taint / etykietę / adnotację | dodać tainta / zalabelować / zaannotować |
| evict | usunąć (pod) z węzła | zrobić evict poda |
| roll out (a change) | wdrożyć | zrobić rollout |
| rolling update | aktualizacja krocząca | rolling update |
| staged / phased rollout | wdrożenie etapowe | wdrożenie etapowe |
| provision | przygotować, utworzyć | sprovisionować |
| upgrade / downgrade | zaktualizować / przywrócić starszą wersję | zupgrade'ować / zdowngrade'ować |
| backup / restore | wykonać kopię zapasową / przywrócić | zrobić backup / przywrócić |
| patch (server) | zaktualizować, załatać | spatchować |
| bootstrap | zainicjować | zbootstrapować |

### Networking and security

| English | Publiczna | Wewnętrzna |
|---|---|---|
| route / forward / proxy | kierować / przekierować / pośredniczyć | zroutować / przeforwardować / puścić przez proxy *(potoczna)* |
| resolve (DNS) | rozwiązać nazwę | rozwiązać |
| allowlist / blocklist | dodać do listy dozwolonych / zablokowanych | dodać do allowlisty / zablokować |
| throttle / rate-limit | ograniczyć przepustowość / liczbę żądań | throttlować / zrate-limitować |
| rotate (secret) | wymienić, zrotować | zrotować secreta |
| revoke | unieważnić | unieważnić, zrevoke'ować |
| hash / encrypt / sign | obliczyć skrót / zaszyfrować / podpisać | zahashować / zaszyfrować / podpisać |
| authenticate / authorize | uwierzytelnić / autoryzować | uwierzytelnić / zautoryzować |
| harden | wzmocnić zabezpieczenia | zhardenować |
| scan | przeskanować | zeskanować |

### Observability and problem solving

| English | Publiczna | Wewnętrzna |
|---|---|---|
| scrape (metrics) | pobierać metryki | scrape'ować |
| instrument | dodać instrumentację | zinstrumentować |
| trace | śledzić | trace'ować |
| ingest (logs) | przyjmować, pobierać | zaingestować |
| query | wykonać zapytanie | odpytać |
| alert / silence | wysłać alert / wyciszyć | zaalertować / wyciszyć |
| investigate | zbadać | zbadać, przeanalizować |
| reproduce | odtworzyć | zreprodukować |
| isolate / narrow down | wyizolować / zawęzić | odizolować / zawęzić |
| rule out | wykluczyć | wykluczyć |
| inspect (logs) | przejrzeć | przejrzeć, przekopać logi *(potoczna)* |
| troubleshoot | diagnozować | zdebugować |
| root-cause analysis | analiza przyczyny źródłowej | analiza root cause, RCA |

## Forms to avoid

These appear in informal lists but are wrong or misleading in any register:

| Avoid | Why | Use |
|---|---|---|
| wyegzekwować (execute) | means *enforce* | wykonać, uruchomić |
| zresolverować | not in use | rozwiązać |
| zinvestygować | not in use | zbadać |
| zautentykować | not in use | uwierzytelnić |
| ztestować, zprovisionować, zpatchować | wrong prefix before voiceless consonant | przetestować, sprovisionować, spatchować |
| zexecute'ować, zdescribe'ować, zreconcilować | unreadable in writing | wykonać, opisać, uzgodnić stan |
| aplikować zmiany (outside `kubectl apply`) | calque | wprowadzić zmiany |
| wyewikować, scordonować, scache'ować | coined, nobody says them | zrobić evict, zrobić cordon, wrzucić do cache'u |
| serwis in the sense of *service*, wolumin, wolumen | phonetic polonization: neither English nor Polish | usługa or `Service`; volume. Fine in other senses: „okno serwisowe”, „serwis techniczny”, „serwis internetowy” |
