from .base import Base
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer, Date

class SpimexTradingResult(Base):
    __tablename__ = 'spimex_trading_results'

    exchange_product_id: Mapped[str] = mapped_column(String, nullable=False)
    exchange_product_name: Mapped[str] = mapped_column(String, nullable=False)
    oil_id: Mapped[str] = mapped_column(String)
    delivery_basis_id: Mapped[str] = mapped_column(String)
    delivery_basis_name: Mapped[str] = mapped_column(String)
    delivery_type_id: Mapped[str] = mapped_column(String)
    volume: Mapped[float] = mapped_column(Float)
    total: Mapped[float] = mapped_column(Float)
    count: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime.date] = mapped_column(Date)
