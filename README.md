# Premier Properties - Real Estate Listing App

A full-stack real estate listing application with property search, filtering, map integration, and contact forms.

## Tech Stack

- **Frontend**: React + TypeScript (Vite)
- **Backend**: Python + FastAPI
- **Database**: PostgreSQL
- **Maps**: Leaflet + OpenStreetMap

## Quick Start (Docker)

```bash
docker compose up --build
```

This starts:
- PostgreSQL on port 5432
- Backend API on http://localhost:8000
- Frontend on http://localhost:5173

The database is automatically seeded with 15 sample property listings.

## Manual Setup

### Database

Start a PostgreSQL instance with:
- Database: `realestate`
- User: `realestate`
- Password: `realestate`

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
RUN_SEED=true python seed.py   # seed sample data (set RUN_SEED=true)
uvicorn app.main:app --reload     # start API server on :8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev    # start dev server on :5173
```

## API Endpoints

| Method | Endpoint             | Description                        |
|--------|---------------------|------------------------------------|
| GET    | /api/properties      | List properties (with filters)     |
| GET    | /api/properties/:id  | Get a single property              |
| POST   | /api/contact         | Submit a contact inquiry           |
| GET    | /api/health          | Health check                       |

### Filter Query Parameters

- `search` — free text search across title, description, address, city
- `min_price` / `max_price` — price range
- `city` — filter by city name
- `bedrooms` — minimum bedrooms
- `property_type` — House, Condo, Townhouse, Apartment, Land, Commercial

## Features

- Responsive property grid with card layout
- Filter/search by price range, city, bedrooms, and property type
- Property detail modal with photo gallery
- Contact form for inquiries on individual properties
- Interactive map view with property markers (Leaflet + OpenStreetMap)
- Mobile-responsive design
- 15 pre-loaded sample listings across the US
