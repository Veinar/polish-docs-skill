# Pierwsze kroki z datasync

datasync synchronizuje tabele między dwiema bazami PostgreSQL – w jednym przebiegu i z możliwością wznowienia.

## Instalacja

```bash
npm install -g datasync
```

## Uruchomienie synchronizacji

Ustaw adres bazy w zmiennej `DATASYNC_DATABASE_URL`, a potem uruchom:

```bash
datasync sync --database-url=<databaseUrl> --batch-size=<batchSize>
```

Zastąp `<databaseUrl>` adresem bazy źródłowej. Wynik powinien zawierać wiersz „Synced 12 tables”.

## Rozwiązywanie problemów

Jeśli synchronizacja kończy się kodem 3, zdeployuj wersję z poprawką lub zrestartuj worker. Więcej w [słowniku](slownik.md).
