from .database import Base
from sqlalchemy import Column, DateTime, Integer, Float, Text, String
from sqlalchemy.sql import func


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String(50), nullable=False, unique=True)
    query = Column(Text, nullable=False)
    time_to_execute_in_mins = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
