#
#
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect
from models.spimex_trading_result import SpimexTradingResult


class SpimexTradingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_many(self, records: list[dict], batch_size: int = 1000) -> int:
        total_saved = 0
        try:

            columns = [
                        column.name
                        for column in inspect(SpimexTradingResult).mapper.columns
                        if column.name not in {"id"}
                    ]

            conn = await self.session.connection()
            raw_conn = await conn.get_raw_connection()
            asyncpg_conn = raw_conn.driver_connection # это сам asyncpg.Connection

            for i in range(0, len(records), batch_size):
                    batch = records[i:i + batch_size]

                    # Преобразуем в list[tuple], соблюдая порядок колонок
                    tuples = [tuple(rec[col] for col in columns) for rec in batch]

                    await asyncpg_conn.copy_records_to_table(   #type: ignore[attr-defined]
                        table_name=SpimexTradingResult.__tablename__,
                        records=tuples,
                        columns=columns
                    )

                    total_saved += len(batch)

            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            print(f"Ошибка при сохранении: {e}")

        return total_saved
