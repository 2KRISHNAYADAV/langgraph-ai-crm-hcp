from sqlalchemy import Column, Integer, String, Text
from database.database import Base

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String, index=True)
    date = Column(String)
    product = Column(String)
    notes = Column(Text)
    sentiment = Column(String)
    follow_up = Column(String)
