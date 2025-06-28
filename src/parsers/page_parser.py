from datetime import datetime
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

from parsers.base import BaseParser


class SpimexPageParser(BaseParser):
    BASE_URL = "https://spimex.com/markets/oil_products/trades/results/"

    def parse(self, raw_input: Any = None) -> list[dict]:
        results = []
        next_page_url = self.BASE_URL

        while next_page_url:
            response = requests.get(next_page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")

            items = soup.select(".accordeon-inner__item")
            for item in items:
                link_tag = item.select_one("a.accordeon-inner__item-title.link.xls")
                date_tag = item.select_one(".accordeon-inner__item-inner__title span")

                if link_tag and date_tag:
                    href = urljoin(self.BASE_URL, str(link_tag.get("href")))
                    date_text = date_tag.get_text(strip=True)

                    date_obj = self._parse_date(date_text)
                    if date_obj and 2023 <= date_obj.year <= 2025:
                        results.append({"url": href, "date": date_obj})

            next_page_url = self._get_next_page_url(soup, current_url=next_page_url)

        return results

    def _parse_date(self, date_text: str):
        try:
            date_part = date_text.split()[0]
            return datetime.strptime(date_part, "%d.%m.%Y").date()
        except Exception:
            return None

    def _get_next_page_url(self, soup: BeautifulSoup, current_url: str) -> str | None:
        pagination_container = soup.select_one("div.bx-pagination-container ul")
        if not pagination_container:
            return None

        next_li = pagination_container.select_one("li.bx-pag-next")
        if not next_li:
            return None

        a_tag = next_li.find("a")
        if not a_tag or not isinstance(a_tag, Tag):
            return None

        href = a_tag.get("href")
        if href and isinstance(href, str):
            return urljoin(current_url, href)
        return None
