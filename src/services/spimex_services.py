import requests
from sqlalchemy.exc import SQLAlchemyError

from database.db import SessionLocal
from models.spimex_trading_result import SpimexTradingResult
from parsers.excel_parser import SpimexExcelParser
from parsers.page_parser import SpimexPageParser


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
            for rec in records:
                obj = SpimexTradingResult(**rec)
                session.add(obj)
            session.commit()
            print(f"Сохранено {len(records)} записей")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Ошибка при сохранении: {e}")
        finally:
            session.close()
