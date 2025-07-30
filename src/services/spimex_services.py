# import httpx

# from database.db import SessionLocal
# from parsers.excel_parser import SpimexExcelParser
# from parsers.page_parser import SpimexPageParser
# from repositories.spimex_repo import SpimexTradingRepository
# from schemas.trading_result import TradingResultSchema

# class SpimexTradingService:
#     def __init__(self):
#         self.page_parser = SpimexPageParser()
#         self.excel_parser = SpimexExcelParser()

#     async def run(self):
#         bulletins = await self.page_parser.parse()

#         async with httpx.AsyncClient() as client:
#             for bulletin in bulletins:
#                 url = bulletin["url"]
#                 date_str = bulletin["date"]

#                 print(f"Обработка бюллетеня за {date_str}: {url}")

#                 try:
#                     response = await client.get(url)
#                     response.raise_for_status()

#                     records = self.excel_parser.parse(response.content)
#                     await self._save_to_db(records)

#                 except Exception as e:
#                     print(f"Ошибка при обработке {url}: {e}")

#     async def _save_to_db(self, records: list[dict]):
#         async with SessionLocal() as session:
#             valid_records = []
#             for rec in records:
#                 try:
#                     rec_model = TradingResultSchema(**rec)
#                     valid_records.append(rec_model.model_dump())
#                 except Exception as e:
#                     print(f"Ошибка валидации: {e}")

#             repo = SpimexTradingRepository(session)
#             await repo.save_many(valid_records, batch_size=1000)
#             print(f"Сохранено {len(valid_records)} записей")


import httpx
from datetime import datetime, timezone

from database.db import SessionLocal
from parsers.excel_parser import SpimexExcelParser
from parsers.page_parser import SpimexPageParser
from repositories.spimex_repo import SpimexTradingRepository
from schemas.trading_result import TradingResultSchema


class SpimexTradingService:
    def __init__(self):
        self.page_parser = SpimexPageParser()
        self.excel_parser = SpimexExcelParser()

    async def run(self):
        bulletins = await self.page_parser.parse()

        async with httpx.AsyncClient() as client:
            for bulletin in bulletins:
                url = bulletin["url"]
                date_str = bulletin["date"]

                print(f"Обработка бюллетеня за {date_str}: {url}")

                try:
                    response = await client.get(url)
                    response.raise_for_status()

                    records = self.excel_parser.parse(response.content)
                    await self._save_to_db(records)

                except Exception as e:
                    print(f"Ошибка при обработке {url}: {e}")

    async def _save_to_db(self, records: list[dict]):
        async with SessionLocal() as session:
            valid_records = []
            now = datetime.now(timezone.utc)

            for rec in records:
                try:
                    rec_model = TradingResultSchema(**rec)
                    rec_dict = rec_model.model_dump()

                    # Добавляем audit-поля, которые требуются при вставке
                    rec_dict["created_on"] = now
                    rec_dict["updated_on"] = now

                    valid_records.append(rec_dict)
                except Exception as e:
                    print(f"Ошибка валидации: {e}")

            if valid_records:
                repo = SpimexTradingRepository(session)
                await repo.save_many(valid_records, batch_size=1000)
                print(f"Сохранено {len(valid_records)} записей")
            else:
                print("Нет валидных записей для сохранения.")
