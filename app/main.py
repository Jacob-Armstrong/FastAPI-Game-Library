from fastapi import FastAPI
from .database import engine
from .models import Base

from .routers import games, publishers

# Create tables from .models
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(games.router)
app.include_router(publishers.router)

@app.get("/")
async def root():
    return {
        "Indroduction": "Welcome to this simple FastAPI Project! Check out the games in /games, or their publishers in /publishers!",
        "Created By": "Jacob Armstrong",
        "Using": "FastAPI, Pydantic, SQLAlchemy & PostgreSQL",
        "Documentation": "127.0.0.1:8000/docs"
        }