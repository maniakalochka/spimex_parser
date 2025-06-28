from pydantic import BaseModel
from datetime import datetime


class TradingResultSchema(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: str
    total: float
    count: int
    date: datetime
