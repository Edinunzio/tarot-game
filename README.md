# Tarot

A local tarot reading app for personal entertainment. Everything runs in Docker — nothing needs to be installed on your machine.

## Stack

| Layer    | Technology |
|----------|------------|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS 3 |
| Backend  | Django 5.1 + Django REST Framework |
| Database | PostgreSQL 16 |
| LLM *(planned)* | Ollama + Mistral 7B |

## Features

- Rider-Waite deck (78 cards, full Major and Minor Arcana)
- Three Card spread (Past / Present / Future)
- Custom shuffling algorithms that simulate physical handling: overhand, riffle, and cut
- ~20% per-packet reversal chance during overhand shuffle — reversed cards emerge naturally
- Position-aware interpretations (each card's meaning is contextualised to its spread position)
- Card flip animations
- Django admin for browsing all cards, spreads, and past readings

## Getting Started

### 1. Copy the env file

```bash
cp .env.example .env
```

The defaults in `.env.example` work as-is for local development.

### 2. Start all containers

```bash
docker compose up --build
```

This starts three services:
- `frontend` → http://localhost:5173
- `backend`  → http://localhost:8000
- `db`       → PostgreSQL on port 5432

The backend entrypoint waits for the database to be ready, then runs migrations automatically.

### 3. Seed the deck

```bash
docker compose exec backend python manage.py seed_deck
```

Loads the full 78-card Rider-Waite deck and the Three Card spread into the database.

To reseed from scratch:

```bash
docker compose exec backend python manage.py seed_deck --clear
```

### 4. (Optional) Create an admin user

```bash
docker compose exec backend python manage.py createsuperuser
```

Admin interface: http://localhost:8000/admin

## Project Structure

```
tarot-game/
├── docker-compose.yml
├── .env                        # local secrets — gitignored
├── .env.example                # template
│
├── backend/
│   ├── Dockerfile
│   ├── entrypoint.sh           # waits for db, runs migrate, starts server
│   ├── requirements.txt
│   ├── manage.py
│   ├── config/                 # Django project settings, urls, wsgi
│   └── tarot/
│       ├── models.py           # Deck, Card, Spread, SpreadPosition, Reading, ReadingCard
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── shuffle.py          # overhand, riffle, cut, full_shuffle
│       ├── admin.py
│       └── management/commands/
│           └── seed_deck.py    # seeds Rider-Waite + Three Card spread
│
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.ts          # proxies /api → backend:8000
    └── src/
        ├── types/api.ts        # TypeScript interfaces
        ├── services/api.ts     # fetch wrappers
        ├── pages/
        │   ├── HomePage.tsx    # question form + deck/spread selectors
        │   ├── ShufflePage.tsx # shuffle animation + cut the deck
        │   └── ReadingPage.tsx # card reveal + interpretations
        └── components/
            └── CardSlot.tsx    # card with 3D flip animation
```

## API

```
GET  /api/decks/              list all decks
GET  /api/spreads/            list spreads with positions
POST /api/readings/           create a reading  { deck_id, spread_id, question }
GET  /api/readings/<id>/      retrieve a reading with all cards and interpretations
```

## Shuffling

The shuffle sequence for each reading is:

```
overhand × 5  →  riffle × 2  →  cut  →  overhand × 2  →  cut
```

**Overhand shuffle** — takes random-sized packets (3–12 cards) from the top and places them on a growing pile. Each packet has a ~20% chance of being physically flipped, introducing reversed cards.

**Riffle shuffle** — splits the deck roughly in half (±5 card variance) and interleaves with weighted randomness rather than a perfect alternation.

**Cut** — splits at a random point in the 35–65% range and swaps the halves.

All shuffle functions are pure (no mutation) and live in `backend/tarot/shuffle.py`.

## Gotchas

**Adding a new npm package** requires rebuilding the frontend image and clearing the old `node_modules` volume:

```bash
docker compose rm -sf frontend
docker compose up --build frontend
```

Do **not** use `docker compose down -v` unless you want to wipe the database too — that flag removes all volumes including `pgdata`.

**Migrations** — after changing models, run:

```bash
docker compose exec backend python manage.py makemigrations tarot
docker compose exec backend python manage.py migrate
```

## Roadmap

- [ ] Phase 6: Ollama + Mistral 7B for contextual, question-aware interpretations
- [ ] Additional spreads (Celtic Cross, etc.)
- [ ] Additional decks
- [ ] Card images
