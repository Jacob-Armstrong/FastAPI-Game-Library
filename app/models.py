from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Creates the tables in postgres

class Games(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    rating = Column(Numeric, nullable=False)
    publisher = Column(String, nullable=False)

class Publishers(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    games = Column(String, nullable=False)
