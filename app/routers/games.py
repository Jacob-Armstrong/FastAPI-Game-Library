from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db

from ..models import Games
from ..schemas import GameCreate, GameResponse, GameUpdate

router = APIRouter()

@router.post("/gamers", response_model=GameResponse)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    existing_game = db.query(Games).filter(Games.title == game.title).first()
    if existing_game:
        raise HTTPException(status_code=400, detail=f"{game.title} already exists.")
    
    new_game = Games(**game.model_dump())
    db.add(new_game)
    db.commit()
    db.refresh()
    return new_game

@router.get("/games", response_model=list[GameResponse])
def get_games(db: Session = Depends(get_db)):
    return db.query(Games).all()

@router.get("/games/{title}", response_model=GameResponse)
def get_game_by_title(title: str, db: Session = Depends(get_db)):
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