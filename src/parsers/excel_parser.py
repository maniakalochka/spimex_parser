import re
from io import BytesIO

import pandas as pd
from pydantic import ValidationError

from schemas.trading_result import TradingResultSchema

from .base import BaseExcelParser


class SpimexExcelParser(BaseExcelParser):
    def parse(self, raw_input: bytes) -> list[dict]:
        date_str = self.extract_trade_date(raw_input)

        df_full = pd.read_excel(BytesIO(raw_input), engine="xlrd", header=None)

        start_idx = None
        for idx, row in df_full.iterrows():
            if (
                row.astype(str)
                .str.contains("Единица измерения: Метрическая тонна")
                .any()
            ):
                start_idx = idx + 1  # type: ignore
                break

        if start_idx is None:
            raise ValueError(
                "Не найдена таблица с 'Единица измерения: Метрическая тонна'"
            )

        df = pd.read_excel(BytesIO(raw_input), engine="xlrd", header=start_idx)
        df.columns = [self.normalize_column(col) for col in df.columns]

        results = []
        for _, row in df.iterrows():
            raw_count = row.get("количество_договоров_шт")

            if raw_count is None or pd.isna(raw_count):
                continue

            try:
                count = int(float(str(raw_count).replace(",", ".")))
            except (ValueError, TypeError):
                continue

            if count < 1:
                continue

            exchange_product_id = row.get("код_инструмента")

            if "итого" in str(exchange_product_id).lower():
                continue
            result = {
                "exchange_product_id": exchange_product_id,
                "exchange_product_name": row.get("наименование_инструмента"),
                "oil_id": self.generate_oil_id(row.get("код_инструмента")),  # type: ignore
                "delivery_basis_id": self.generate_delivery_basis_id(row.get("код_инструмента")),  # type: ignore
                "delivery_basis_name": row.get("базис_поставки"),
                "delivery_type_id": self.generate_delivery_type_id(row.get("код_инструмента")),  # type: ignore
                "volume": row.get("объем_договоров_в_единицах_измерения"),
                "total": row.get("обьем_договоров_руб"),
                "count": row.get("количество_договоров_шт"),
                "date": pd.to_datetime(date_str, dayfirst=True).date(),
            }
            try:
                validated = TradingResultSchema(**result)
                results.append(validated.model_dump())
            except ValidationError as e:
                print(f"Ошибка валидации строки: {e}")
                continue
        return results

    @staticmethod
    def normalize_column(name: str) -> str:
        if pd.isna(name):
            return "unnamed"
        name = str(name).strip().lower()
        name = name.replace("\n", " ")
        name = re.sub(r"[^\w\s]", "", name)
        name = re.sub(r"\s+", "_", name)
        return name

    @staticmethod
    def extract_trade_date(raw_input: bytes) -> str:
        df = pd.read_excel(BytesIO(raw_input), engine="xlrd", header=None)
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
