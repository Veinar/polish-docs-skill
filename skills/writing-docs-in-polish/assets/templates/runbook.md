<!-- Rejestr: inżynierska – naturalny żargon zespołu (zdeployuj, zrollbackuj, pod, deployment). Pisz dla osoby obudzonej o 3:00: krótkie zdania, gotowe polecenia do skopiowania, jasne kryteria eskalacji. -->
# Runbook: <problem lub alert, np. „Wysoki odsetek błędów 5xx w payments-api”>

- Właściciel: <zespół>
- Alert: `<nazwa_alertu>`
- Ostatnia weryfikacja: <RRRR-MM-DD>

## Kiedy użyć

<Objawy i alerty, które kierują do tego runbooka.>

## Wymagania

- Dostęp do <klastra / konsoli / VPN>
- Uprawnienia: <rola>

## Diagnoza

1. Sprawdź status podów:

   ```bash
   kubectl -n <namespace> get pods -l app=<aplikacja>
   ```

   Jeśli pody są w stanie `CrashLoopBackOff`, przejdź do kroku 2. Jeśli wszystkie są `Running`, przejdź do kroku 3.

2. Przejrzyj logi poda:

   ```bash
   kubectl -n <namespace> logs <nazwa_poda> --previous
   ```

3. <Kolejny krok diagnozy.>

## Naprawa

### Wariant A: <przyczyna, np. „nieudany deployment”>

Zrollbackuj deployment do poprzedniej wersji:

```bash
kubectl -n <namespace> rollout undo deployment/<nazwa>
```

### Wariant B: <inna przyczyna>

## Ograniczenia

<!-- Czego naprawa NIE cofa lub nie obejmuje, np. rollout undo nie cofa zmian w ConfigMap/Secret ani migracji bazy danych. -->
- <…>

## Weryfikacja

<Jak potwierdzić, że problem ustąpił, np. metryka wróciła poniżej progu.>

## Eskalacja

Jeśli po <N> minutach problem nie ustąpi, eskaluj do <zespół / dyżur> na <kanał>.

## Powiązane

- [<Dashboard>](<link>)
- [<Postmortem z podobnego incydentu>](<link>)
