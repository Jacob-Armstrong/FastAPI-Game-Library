from fastapi import APIRouter, HTTPException, Depends
from ..models import Publishers
from ..schemas import PublisherCreate, PublisherResponse
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
def get_publishers(db: Session = Depends(get_db)):
    return db.query(Publishers).all()

@router.get("/publishers/{name}", response_model=PublisherResponse)
def get_publisher_by_name(name: str, db: Session = Depends(get_db)):
    publisher = db.query(Publishers).filter(Publishers.name == name).first()
    if not publisher:
        raise HTTPException(status_code=404, detail=f"{name} not found.")
    return publisher