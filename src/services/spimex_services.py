import requests

from database.db import SessionLocal
from parsers.excel_parser import SpimexExcelParser
from parsers.page_parser import SpimexPageParser
from repositories.spimex_repo import SpimexTradingRepository
from schemas.trading_result import TradingResultSchema


class SpimexTradingService:

    def __init__(self):
        self.page_parser = SpimexPageParser()
        self.excel_parser = SpimexExcelParser()

    def run(self):
        bulletins = self.page_parser.parse()

        for bulletin in bulletins:
            url = bulletin["url"]
            date_str = bulletin["date"]

            print(f"Обработка бюллетеня за {date_str}: {url}")

            try:
                response = requests.get(url)
                response.raise_for_status()

                records = self.excel_parser.parse(response.content)

                self._save_to_db(records)

            except Exception as e:
                print(f"Ошибка при обработке {url}: {e}")

    def _save_to_db(self, records: list[dict]):
        session = SessionLocal()
        try:
            valid_records = []
            for rec in records:
                try:
                    rec_model = TradingResultSchema(**rec)
                    valid_records.append(rec_model.model_dump())
                except Exception as e:
                    print(f"Ошибка валидации: {e}")

            repo = SpimexTradingRepository(session)
            saved = repo.save_many(valid_records, batch_size=1000)
            print(f"Сохранено {saved} записей")
        finally:
            session.close()
