import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import properties, contact

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real Estate Listings API")

allowed_origins = os.environ.get(
    "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(properties.router)
app.include_router(contact.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
