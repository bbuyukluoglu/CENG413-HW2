# HW-2 Answers

<!--
  NOTE TO SELF: the assignment says the answers must be in MY OWN WORDS.
  Replace each "TODO" with 3-6 of my own sentences, then delete the
  "Key points" lists and this comment. The test results below are real
  (I ran them), keep them as evidence.
-->

## 1. How does the app reach the database by name?

TODO (3-6 sentences)

Key points to cover:
- Compose creates a user-defined network for the project (`<project>_default`).
- Docker's embedded DNS on that network resolves the service name `db` to the container IP
  (`docker compose exec app getent hosts db` -> `172.18.0.2  db`).
- The app gets `DB_HOST=db` from `compose.yaml`; no IP or `localhost` (inside the app container `localhost` is the app itself).
- The default `bridge` network used by plain `docker run` has no name-based DNS, so names do not resolve there.

## 2. Which service is stateless, which is not? Evidence

TODO (3-6 sentences)

What I did and what happened (`curl localhost:8000/visit` after each step):

| Step | Result |
|---|---|
| `docker compose up -d --build`, two requests | `{"visits":1}`, `{"visits":2}` |
| `docker compose rm -sf app`, then `docker compose up -d` | `{"visits":3}` (data kept) |
| `docker compose down`, then `docker compose up -d` | `{"visits":4}` (data kept) |
| `docker compose down -v`, then `docker compose up -d` | `{"visits":1}` (data gone) |

Key points to cover:
- `app` is stateless: it writes nothing to its own disk, so deleting the container loses nothing.
- `db` is stateful: its data lives in the named volume `pgdata`.
- `down` removes containers and the network but keeps volumes; `down -v` also deletes the volume.

## 3. Where should a database password come from?

TODO (3-6 sentences)

Key points to cover:
- From the environment at run time: here a `.env` file (ignored by Git) read by Compose as `${DB_PASSWORD}`;
  in production a secret manager / Docker secrets.
- Git history keeps it forever, even after deleting the line; every clone, fork, backup and CI log has it.
- "Private" repos are still shared with many people/tools and can leak or become public later.
- `.env.example` with fake values documents which variables are needed.

## AI usage

TODO (1-2 sentences about how I used an AI assistant)
