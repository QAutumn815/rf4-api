<div align="center">
    <a href="https://github.com/hurfy/rf4-api"><img src="https://github.com/user-attachments/assets/c1890100-fb8b-4ac4-a28d-5b097eb536b9" alt="rf4-api" /></a>
</div>

<div align="center">
    <a href="https://github.com/hurfy/rf4-api/issues"><img src="https://img.shields.io/github/issues/hurfy/rf4-api?style=for-the-badge" alt="open issues" /></a>
    <img src="https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge" alt="version" />
    <a href="LICENSE"><img src="https://img.shields.io/github/license/hurfy/rf4-api?style=for-the-badge" alt="license" /></a>
</div>

<br />

<div align="center">
  Unofficial catch API for Russian Fishing 4
</div>

<div align="center">
  <sub>
    Built with love
    &bull; Brought to you by <a href="https://github.com/hurfy">@hurfy</a>
    and other <a href="https://github.com/hurfy/rf4-api/graphs/contributors">contributors</a>
  </sub>
</div>

---

## 📖 Introduction

**This project is still in development!**

The main objective of this project is the periodic collection of data regarding records, ratings, and winners from the official [Russian Fishing 4](https://rf4game.com) website, followed by processing and presenting it in a convenient format — via both a **REST API** and a **browsable web UI**. The parsing covers all 10 server regions and 3 rod categories (Records, Ultralight, Telestick) for each table.

*I do not own the data but collect it to present in a convenient and accessible format. All rights are reserved by FishSoft LLC.*

---

## ✨ Features

### 📊 Data Collection
| Feature | Description |
|---|---|
| **Absolute Records** | All-time fish records across all regions and categories |
| **Weekly Records** | Weekly fish records (updated weekly per region) |
| **Player Ratings** | Player rankings with level and playtime data |
| **Competition Winners** | Tournament standings with scores and prizes |
| **10 Regions** | GL, RU, DE, US, FR, CN, PL, KR, JP, EN |
| **3 Categories** | Records, Ultralight, Telestick |
| **Fish Image Caching** | Automatically downloads and caches fish icons locally, bypassing hotlink protection |

### 🌐 REST API
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/v1/parse/` | Trigger asynchronous data scraping (via Celery) |
| `DELETE` | `/v1/clear/` | Clear table data |
| `GET` | `/v1/records/abs/{region}/{category}/` | List absolute records |
| `GET` | `/v1/records/wk/{region}/{category}/` | List weekly records |
| `GET` | `/v1/ratings/{region}/` | List player ratings |
| `GET` | `/v1/winners/{region}/{category}/` | List competition winners |

Each `GET` endpoint supports:

- **Filtering** via query parameters — filter by fish, player, location, bait, weight range, date range, position range, level, score, prize, and more
- **Pagination** — `?page=` and `?per_page=` (default 25, max 100)
- **Ordering** — `?ordering=<field>` (any field, prefix `-` for descending)
- **Display transforms** — `?in_gram=true` (records → weight in grams), `?in_days=true` (ratings → playtime in days)

### 🖥️ Browsable Web UI
| Route | Page |
|---|---|
| `/` | Dashboard with stats and API reference |
| `/browse/records/{abs\|wk}/{region}/{category}/` | Browse fish records with filters |
| `/browse/ratings/{region}/` | Browse player ratings with filters |
| `/browse/winners/{region}/{category}/` | Browse competition winners with filters |

### 📚 API Documentation (Auto-generated)
| Route | Type |
|---|---|
| `/docs/` | OpenAPI 3.0 JSON Schema |
| `/docs/swagger/` | Swagger UI |
| `/docs/redoc/` | ReDoc UI |

### 🔧 Admin Interface
Full Django admin at `/admin/` for managing all data models with search, filtering, and date hierarchy.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Web Scraper Layer                       │
│  Selenium Chrome (headless) → HTML → BeautifulSoup → data   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Processing Layer                           │
│  DataProcessor (weight/date cleaning)                       │
│  FishImageCache (download & cache fish icons)               │
│  DBProcessor (atomic bulk write)                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                       Data Layer                              │
│  MySQL Database                                              │
│  Models: AbsoluteRecord, WeeklyRecord, Rating, Winner        │
└──────────┬──────────────────┬──────────────────┬─────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│   REST API      │ │  Browse UI      │ │  API Docs           │
│  (DRF viewsets) │ │  (TemplateView) │ │  (drf-spectacular)  │
└─────────────────┘ └─────────────────┘ └─────────────────────┘
```

### Data Flow

1. **Scraping** — `ParsersManager` orchestrates fetchers & parsers for each data source
2. **Processing** — Raw data is cleaned, converted (weights → kg, dates → ISO), and fish images are cached locally
3. **Storage** — Processed data is bulk-written to MySQL in a single atomic transaction (replaces old data)
4. **Serving** — Both the REST API and the web UI read from the same database

The scraping can run via **Celery workers** (async) or via a **management command** (sync, for one-shot runs without Celery).

---

## 🧰 Tech Stack

| Category | Technology |
|---|---|
| **Framework** | Django 5.1 + Django REST Framework 3.15 |
| **Database** | MySQL (via PyMySQL) |
| **Scraping** | Selenium 4.23 + BeautifulSoup 4 |
| **Task Queue** | Celery 5.4 (Redis broker) |
| **API Docs** | drf-spectacular (OpenAPI 3.0 / Swagger / ReDoc) |
| **Filtering** | django-filter |
| **Config** | python-decouple (.env) |

---

## 🚀 Quick Start

> Currently only development mode is available.

### Prerequisites

- Python 3.10+
- MySQL server
- Redis (for Celery)
- Chrome / Chromium (for Selenium scraping)

### Setup

```shell
# Clone the repository
git clone https://github.com/QAutumn815/rf4-api.git
cd rf4-api

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MySQL credentials and Django secret key

# Run migrations
python manage.py migrate

# Start Django development server
python manage.py runserver

# Start Celery worker (in a separate terminal)
celery -A worker.app worker -l INFO -c 1 -P solo

# Or run a one-time sync scrape (no Celery needed)
python manage.py scrape_all
```

### API Usage Examples

```shell
# Get absolute records for the global region, records category
curl http://localhost:8000/v1/records/abs/gl/records/

# Get weekly records for the US region, ultralight category
curl http://localhost:8000/v1/records/wk/us/ultralight/

# Get player ratings for EU region, filtered by player name
curl "http://localhost:8000/v1/ratings/de/?player=Fisherman"

# Get winners with min score filter
curl "http://localhost:8000/v1/winners/ru/telestick/?min_score=1000"

# Trigger a full data scrape
curl -X POST http://localhost:8000/v1/parse/ \
  -H "Content-Type: application/json" \
  -d '{"tables": ["*"]}'

# Clear all data
curl -X DELETE http://localhost:8000/v1/clear/ \
  -H "Content-Type: application/json" \
  -d '{"tables": ["*"]}'
```

---

## 🌍 Supported Regions

| Code | Region |
|---|---|
| `gl` | Global |
| `ru` | Russia |
| `de` | Germany |
| `us` | USA |
| `fr` | France |
| `cn` | China |
| `pl` | Poland |
| `kr` | South Korea |
| `jp` | Japan |
| `en` | Europe (English) |

## 🎣 Supported Categories

| Slug | Description |
|---|---|
| `records` | Standard records |
| `ultralight` | Ultralight rod records |
| `telestick` | Telestick rod records |

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <sub>
    Built with love
    &bull; Brought to you by <a href="https://github.com/hurfy">@hurfy</a>
    and other <a href="https://github.com/hurfy/rf4-api/graphs/contributors">contributors</a>
  </sub>
  <br />
  <sub>
    <em>All game data belongs to <a href="https://rf4game.com">FishSoft LLC</a>. This project is not affiliated with or endorsed by FishSoft LLC.</em>
  </sub>
</div>
