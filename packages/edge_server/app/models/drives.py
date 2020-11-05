from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from ..database.base import Base

# from ..models.genres import Genres


class Drives(Base):
    __tablename__ = "drives"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    # genre_id = Column(Integer, ForeignKey("genres.id"))
    # genre = relationship(
    #     Genres, backref=backref("drives", uselist=True, cascade="delete,all")
    # )
