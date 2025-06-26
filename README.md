# Как запустить

### Необходимые зависимости

- Python 3.12+
- Poetry 2
- Docker

---

```bash
git clone https://github.com/maniakalochka/spimex_parser.git
cd spimex_parser
docker compose up --build
```

После этих команд, не сразу, а через примерно ~1 минуту в терминале начнется "движ" с сохранением данных в БД.

После успешного занесения в БД можно зайти в контейнере в `psql` и посмотреть данные:

```bash
docker compose exec db psql -U postgres -d spimex_trading_results
```

и выполнить SQL-запрос:

```sql
SELECT
    *
FROM
    spimex_trading_results
WHERE
    date >= '2023-01-01' AND date < '2024-01-01';
```
