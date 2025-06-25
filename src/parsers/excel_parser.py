from .base import BaseParser
import pandas as pd
from io import BytesIO


class SpimexExcelParser(BaseParser):
    def parse(self, raw_input: bytes) -> list[dict]:
        date_str = self.extract_trade_date(raw_input)

        df_full = pd.read_excel(BytesIO(raw_input), engine='xlrd', header=None)

        start_idx = None
        for idx, row in df_full.iterrows():
            if row.astype(str).str.contains("Единица измерения: Метрическая тонна").any():
                start_idx = idx + 1  # type: ignore
                break

        if start_idx is None:
            raise ValueError("Не найдена таблица с 'Единица измерения: Метрическая тонна'")

        df = pd.read_excel(BytesIO(raw_input), engine='xlrd', header=start_idx)

        results = []
        for _, row in df.iterrows():
            count = row.get("Количество\nДоговоров,\nшт.")
            if bool(pd.isna(count)) or str(count).strip() == "-":
                continue

            exchange_product_id = row.get("Код\nИнструмента")
            if bool(pd.isna(exchange_product_id)):
                continue
            result = {
                "exchange_product_id": exchange_product_id,
                "exchange_product_name": row.get("Наименование\nИнструмента"),
                "oil_id": self.generate_oil_id(row.get("Код\nИнструмента")),  # type: ignore
                "delivery_basis_id": self.generate_delivery_basis_id(row.get("Код\nИнструмента")),  # type: ignore
                "delivery_basis_name": row.get("Базис\nПоставки"),
                "delivery_type_id": self.generate_delivery_type_id(row.get("Код\nИнструмента")),  # type: ignore
                "volume": row.get("Объем\nДоговоров\nв единицах\nизмерения"),
                "total": row.get("Обьем\nДоговоров,\nруб."),
                "count": count,
                "date": pd.to_datetime(date_str, dayfirst=True).date(),
            }
            results.append(result)

        return results

    @staticmethod
    def extract_trade_date(raw_input: bytes) -> str:
        df = pd.read_excel(BytesIO(raw_input), engine='xlrd', header=None)
        for row in df.itertuples(index=False):
            for cell in row:
                if isinstance(cell, str) and "Дата торгов" in cell:
                    return cell.split(":")[-1].strip()
        raise ValueError("Не удалось найти ячейку с 'Дата торгов' в отчёте")

    @staticmethod
    def generate_oil_id(exchange_product_id: str) -> str:
        return exchange_product_id[:4]

    @staticmethod
    def generate_delivery_basis_id(exchange_product_id: str) -> str:
        return exchange_product_id[4:7]

    @staticmethod
    def generate_delivery_type_id(exchange_product_id: str) -> str:
        return exchange_product_id[-1]
