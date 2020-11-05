from sqlalchemy.ext.declarative import declarative_base
from .db_session import db_session

Base = declerative_base()
Base.query = db_session.query_property()
