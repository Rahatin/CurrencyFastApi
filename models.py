from sqlalchemy import Column, Integer, String, Float
from database import Base

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    abbreviation = Column(String, nullable=False, unique=True)
    buy_rate = Column(Float, nullable=False)
    sell_rate = Column(Float, nullable=False)

