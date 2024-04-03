from sqlalchemy import Integer, Column, String
from database import Base

class WordCount(Base):
    __tablename__ = 'wordcount'

    word = Column(String, primary_key=True)
    count = Column(Integer, index=True)
