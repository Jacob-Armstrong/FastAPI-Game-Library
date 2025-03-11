from pydantic import BaseModel
from typing import List, Optional

# ================================
# =             Game             =
# ================================

# Base Model
class GameBase(BaseModel):
    title: str
    description: str
    rating: float
    publisher: str

class GameCreate(GameBase):
    pass

# Include ID when returning full record
class GameResponse(GameBase):
    id: int

    class Config:
        orm_mode = True

# Must include title in update -- other columns are optional
class GameUpdate(GameBase):
    description: Optional[str] = None
    rating: Optional[float] = None

# =====================================
# =             Publisher             =
# =====================================

# Base model
class PublisherBase(BaseModel):
    name: str
    description: str
    games: str

class PublisherCreate(PublisherBase):
    pass

# Respond with 
class PublisherResponse(PublisherBase):
    id: int
    games: List[GameResponse] = []

    class Config:
        orm_mode = True

class PublisherUpdate(PublisherBase):
    description: Optional[str] = "Description goes here."
