from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db

from ..models import Games
from ..schemas import GameCreate, GameResponse, GameUpdate

router = APIRouter()

@router.post("/games", response_model=GameResponse)
def create_game(
    game: GameCreate, 
    db: Session = Depends(get_db)
    ):

    existing_game = db.query(Games).filter(Games.title == game.title).first()

    if existing_game:
        raise HTTPException(status_code=400, detail=f"{game.title} already exists.")
    
    new_game = Games(**game.model_dump())

    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return new_game

@router.get("/games", response_model=list[GameResponse])
def get_games(
    description: str | None = Query(default=None, description="(optional) Search for keywords in the descriptions"), 
    publisher: str | None = Query(default=None, description="(optional) Search for games by publisher"),
    db: Session = Depends(get_db)
    ):

    games = db.query(Games)

    if description:
        games = games.filter(Games.description.ilike(f'%{description}%'))
    
    if publisher:
        games = games.filter(Games.publisher.ilike(f'%{publisher}%'))

    games = games.all()
    
    if not games:
        raise HTTPException(status_code=404, detail=f'No games found matching the provided parameters.')

    return games

@router.get("/games/{title}", response_model=GameResponse)
def get_game_by_title(
    title: str, 
    db: Session = Depends(get_db)
    ):

    game = db.query(Games).filter(Games.title == title).first()

    if not game:
        raise HTTPException(status_code=404, detail=f"{title} not found.")
    
    return game

@router.put("/games/{title}", response_model=GameResponse)
def update_game(title: str, game_update: GameUpdate, db: Session = Depends(get_db)):
    game = db.query(Games).filter(Games.title == title).first()

    if not game:
        raise HTTPException(status_code=404, detail=f"{title} not found.")
    
    if game_update.title:
        game.title = game_update.title
    if game_update.description:
        game.description = game_update.description
    if game_update.rating:
        game.rating = game_update.rating
    
    db.commit()
    db.refresh(game)
    return game

@router.delete("/games/{title}", response_model=GameResponse)
def delete_game(title: str, db: Session = Depends(get_db)):
    game = db.query(Games).filter(Games.title == title).first()

    if not game:
        raise HTTPException(status_code=404, detail=f"{title} not found.")
    
    db.delete(game)
    db.commit()
    return game