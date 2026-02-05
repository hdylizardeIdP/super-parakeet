from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import properties, contact

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real Estate Listings API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(properties.router)
app.include_router(contact.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
