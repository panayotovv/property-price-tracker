from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Property(Base):
    __tablename__ = "property"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    location = Column(String)
    link = Column(String, unique=True)

    history = relationship("PropertyHistory", back_populates="property", cascade="all, delete-orphan")


class PropertyHistory(Base):
    __tablename__ = "property_history"

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("property.id"))

    price = Column(Integer)
    area = Column(Float)
    scraped_at = Column(DateTime, default=datetime.utcnow)

    property = relationship("Property", back_populates="history")
