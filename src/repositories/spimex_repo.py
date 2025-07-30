from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from models.spimex_trading_result import SpimexTradingResult


class SpimexTradingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_many(self, records: list[dict], batch_size: int = 1000) -> int:
        total_saved = 0

        try:
            for i in range(0, len(records), batch_size):
                batch = records[i : i + batch_size]
                stmt = insert(SpimexTradingResult).values(batch)
                await self.session.execute(stmt)
                total_saved += len(batch)

            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка при сохранении: {e}")

        return total_saved
