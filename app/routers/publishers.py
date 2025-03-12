from fastapi import APIRouter, HTTPException, Depends
from ..models import Publishers
from ..schemas import PublisherCreate, PublisherResponse, PublisherUpdate
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.post("/publishers", response_model=PublisherResponse)
def create_publisher(publisher: PublisherCreate, db: Session = Depends(get_db)):
    existing_publisher = db.query(Publishers).filter(Publishers.name == publisher.name).first()
    if existing_publisher:
        raise HTTPException(status_code=400, detail=f"{publisher.name} already exists.")

    new_publisher = Publishers(**publisher.model_dump())
    db.add(new_publisher)
    db.commit()
    db.refresh(new_publisher)
    return new_publisher

@router.get("/publishers", response_model=list[PublisherResponse])
def get_publishers(description: str | None = None, games: str | None = None, db: Session = Depends(get_db)):

    publishers = db.query(Publishers)

    if description:
        publishers = publishers.filter(Publishers.description.ilike(f'%{description}%'))

    if games:
        gameList = games.split(', ')
        for game in gameList:
           publishers = publishers.filter(Publishers.games.ilike(f'%{game}%'))
    
    publishers = publishers.all()

    if not publishers:
        raise HTTPException(status_code=404, detail=f'No publishers found matching the provided parameters.')

    return publishers

@router.get("/publishers/{name}", response_model=PublisherResponse)
def get_publisher_by_name(name: str, db: Session = Depends(get_db)):
    publisher = db.query(Publishers).filter(Publishers.name == name).first()
    if not publisher:
        raise HTTPException(status_code=404, detail=f"{name} not found.")
    return publisher

@router.put("/publishers/{name}", response_model=PublisherResponse)
def update_publisher(name: str, publisher_update: PublisherUpdate, db: Session = Depends(get_db)):
    publisher = db.query(Publishers).filter(Publishers.name == name).first()
    if not publisher:
        raise HTTPException(status_code=404, detail=f"{name} not found.")
    
    if publisher_update.name:
        publisher.name = publisher_update.name
    if publisher_update.description:
        publisher.description = publisher_update.description
    if publisher_update.games:
        publisher.games = publisher_update.games

    db.commit()
    db.refresh(publisher)
    return publisher

@router.delete("/publishers/{name}", response_model=PublisherResponse)
def delete_publisher(name: str, db: Session = Depends(get_db)):
    publisher = db.query(Publishers).filter(Publishers.name == name).first()
    if not publisher:
        raise HTTPException(status_code=404, detail=f"{name} not found.")
    
    db.delete(publisher)
    db.commit()
    return publisher