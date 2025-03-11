from pydantic import BaseModel
from typing import List, Optional

# Base Game Model
class GameBase(BaseModel):
    title: str
    description: str
    rating: float

class GameCreate(GameBase):
    pass

# Include ID when returning full record
class GameResponse(GameBase):
    id: int

    class Config:
        orm_mode = True

class GameUpdate(GameBase):
    description: Optional[str] = None
    rating: Optional[float] = None

class PublisherBase(BaseModel):
    name: str
    description: str

class PublisherCreate(PublisherBase):
    pass

class PublisherResponse(PublisherBase):
    id: int
    games: List[GameResponse] = []

    class Config:
        orm_mode = True

class PublisherUpdate(PublisherBase):
    description: Optional[str] = "Description goes here."
