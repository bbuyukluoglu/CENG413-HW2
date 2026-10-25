# CENG413 HW-2: Two Services with Docker Compose

A Flask app (`app`) and PostgreSQL (`db`). The `/visit` counter is stored in PostgreSQL.

Start the whole system (from the project folder):

```bash
cp .env.example .env               # then edit DB_PASSWORD in .env
docker compose up -d --build
docker compose ps                  # db must show (healthy)
curl http://localhost:8000/visit   # {"visits":1}, then 2, 3, ...
```

Stop: `docker compose down` (keeps data) · `docker compose down -v` (deletes data).
