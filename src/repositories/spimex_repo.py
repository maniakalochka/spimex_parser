from sqlalchemy.orm import Session, class_mapper
from sqlalchemy.exc import SQLAlchemyError

from models.spimex_trading_result import SpimexTradingResult


class SpimexTradingRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_many(self, records: list[dict], batch_size: int = 1000) -> int:
        total_saved = 0

        try:
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                self.session.bulk_insert_mappings(
                    class_mapper(SpimexTradingResult), batch
                )
                self.session.commit()
                total_saved += len(batch)
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Ошибка при сохранении: {e}")
        return total_saved
