# CLAUDE.md

This file provides guidance for AI assistants working with the Premier Properties codebase — a full-stack real estate listing application.

## Project Overview

A real estate listing app with property search, filtering, map view, and contact inquiry functionality. The stack is React/TypeScript (frontend), FastAPI/Python (backend), and PostgreSQL (database), all containerized with Docker Compose.

## Repository Structure

```
├── backend/                  # FastAPI backend (Python 3.12)
│   ├── app/
│   │   ├── models/           # SQLAlchemy ORM models (property.py, contact.py)
│   │   ├── routers/          # API route handlers (properties.py, contact.py)
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── config.py         # Settings via pydantic-settings
│   │   ├── database.py       # SQLAlchemy engine and session setup
│   │   └── main.py           # FastAPI app entry point, CORS, router mounting
│   ├── seed.py               # Seeds database with 15 sample properties
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile
├── frontend/                 # React 19 + TypeScript + Vite 7
│   ├── src/
│   │   ├── components/       # React components (one per file)
│   │   │   ├── FilterBar.tsx
│   │   │   ├── PropertyCard.tsx
│   │   │   ├── PropertyDetail.tsx
│   │   │   ├── PropertyMap.tsx
│   │   │   └── ContactForm.tsx
│   │   ├── types/property.ts # Shared TypeScript interfaces
│   │   ├── api/client.ts     # Centralized API client functions
│   │   ├── App.tsx           # Root component, state management
│   │   ├── App.css           # Application styles (CSS variables)
│   │   └── index.css         # Global styles, CSS custom properties
│   ├── vite.config.ts
│   ├── tsconfig.json         # Base TS config (references app + node)
│   ├── tsconfig.app.json     # App TS config (ES2022, strict, react-jsx)
│   ├── tsconfig.node.json    # Node TS config for build tooling
│   ├── eslint.config.js      # ESLint 9 flat config
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml        # Orchestrates all three services
└── README.md
```

## Quick Start

**Docker Compose (recommended):**
```bash
docker compose up --build
```
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- PostgreSQL: port 5432

**Manual setup:**
```bash
# Backend
cd backend && pip install -r requirements.txt
# Set DATABASE_URL in .env (see .env.example)
python seed.py && uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm run dev
```

## Build & Lint Commands

### Frontend (`/frontend`)
| Command | Description |
|---------|-------------|
| `npm run dev` | Start Vite dev server (port 5173) |
| `npm run build` | TypeScript check (`tsc -b`) then Vite production build |
| `npm run lint` | Run ESLint on entire frontend |
| `npm run preview` | Preview production build locally |

### Backend (`/backend`)
| Command | Description |
|---------|-------------|
| `uvicorn app.main:app --reload` | Start FastAPI dev server (port 8000) |
| `python seed.py` | Seed database with sample data |

## Testing

No test framework is currently configured. There are no test files, test dependencies, or test scripts.

## API Endpoints

Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/properties` | List properties (supports filtering) |
| GET | `/api/properties/{id}` | Get single property by ID |
| POST | `/api/contact` | Submit a contact inquiry |
| GET | `/api/health` | Health check |

**Filter query params for GET `/api/properties`:**
`search`, `min_price`, `max_price`, `city`, `state`, `bedrooms`, `property_type`

## Data Models

### Property (backend/app/models/property.py)
Key fields: `id`, `title`, `description`, `price` (integer), `address`, `city`, `state`, `zip_code`, `bedrooms`, `bathrooms` (float), `square_footage`, `property_type` (enum), `listing_status` (enum), `photos` (JSON array), `latitude`, `longitude`.

**PropertyType enum:** House, Condo, Townhouse, Apartment, Land, Commercial
**ListingStatus enum:** Active, Pending, Sold

### ContactInquiry (backend/app/models/contact.py)
Fields: `id`, `property_id` (FK), `name`, `email`, `phone`, `message`, `created_at`

## Code Conventions

### Naming
- **React components:** PascalCase filenames and exports (`PropertyCard.tsx`)
- **TypeScript variables/functions:** camelCase (`fetchProperties`, `handleSubmit`)
- **Python classes/models:** PascalCase (`Property`, `ContactInquiry`)
- **Python functions/variables:** snake_case (`get_db`, `create_inquiry`)
- **Enum values:** UPPER_SNAKE_CASE in Python, mapped to display strings

### Architecture Patterns
- **Frontend state:** Local React hooks (`useState`), no external state library
- **API client:** All fetch calls centralized in `src/api/client.ts`
- **Backend dependency injection:** `Depends(get_db)` for database sessions
- **Schema separation:** Pydantic schemas (validation) separate from SQLAlchemy models (ORM)
- **Router organization:** One router file per resource under `app/routers/`

### File Organization
- One React component per file in `src/components/`
- TypeScript interfaces centralized in `src/types/property.ts`
- Backend follows models → schemas → routers layering
- CSS uses custom properties defined in `index.css`, component styles in `App.css`

### Styling
- CSS custom properties for theming (colors, spacing, shadows)
- Primary color: `#1a56db`, status colors: green (active), amber (pending), red (sold)
- Font: Inter, system-ui fallback
- Responsive grid layout with breakpoints at 768px and 480px
- Mobile-first approach

## Environment Variables

| Variable | Where | Default |
|----------|-------|---------|
| `DATABASE_URL` | Backend | `postgresql://realestate:realestate@db:5432/realestate` |
| `VITE_API_URL` | Frontend | `http://localhost:8000` |

Docker Compose sets these automatically. For local dev, copy `backend/.env.example` to `backend/.env`.

## Key Dependencies

**Frontend:** React 19, Vite 7, TypeScript 5.9, Leaflet + react-leaflet (maps), ESLint 9 with TypeScript plugin
**Backend:** FastAPI 0.115, SQLAlchemy 2.0, Pydantic 2.10, Uvicorn, Alembic 1.14, psycopg2-binary

## Common Tasks

**Add a new API endpoint:** Create or edit a router in `backend/app/routers/`, add Pydantic schemas in `backend/app/schemas/`, register the router in `backend/app/main.py`.

**Add a new frontend component:** Create a `.tsx` file in `frontend/src/components/`, define prop types inline or in `frontend/src/types/property.ts`, import in `App.tsx`.

**Add a new database model:** Create model in `backend/app/models/`, add corresponding schema in `backend/app/schemas/`, update `seed.py` if sample data is needed.

**Modify filters:** Update `PropertyFilter` schema in `backend/app/schemas/property.py`, update query logic in `backend/app/routers/properties.py`, update `FilterBar.tsx` UI.
