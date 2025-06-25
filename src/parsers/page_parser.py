import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from parsers.base import BaseParser
from typing import Any



class SpimexPageParser(BaseParser):
    BASE_URL = "https://spimex.com/markets/oil_products/trades/results/"

    def parse(self, raw_input: Any = None) -> list[dict]:
        response = requests.get(self.BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")

        items = soup.select(".accordeon-inner__item")
        results = []

        for item in items:
            link_tag = item.select_one("a.accordeon-inner__item-title.link.xls")
            date_tag = item.select_one(".accordeon-inner__item-inner__title span")

            if link_tag and date_tag:
                href = urljoin(self.BASE_URL, str(link_tag.get("href")))
                date = date_tag.get_text(strip=True)
                results.append({"url": href, "date": date})

        return results
