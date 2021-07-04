import logging
from decimal import Decimal, InvalidOperation
from typing import Iterator

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from .raw_offer import RawOffer
from .screenshot import make_screenshot_from_html

logger = logging.getLogger(__name__)


CATEGORIES = [
    {
        'category_name': 'Плиты перекрытий',
        'category_url': 'https://zbk56.ru/produkciya/plity-perekrytij.html',
        'delivery_cost': Decimal('1345.00'),
        'measure_unit': 'шт.'
    },
    {
        'category_name': 'Блоки бетонные для стен подвалов (ФБС)',
        'category_url': 'https://zbk56.ru/produkciya/bloki-betonnye-dlya-sten-podvalov-fbs.html',
        'delivery_cost': Decimal('1276.00'),
        'measure_unit': 'шт.'
    }
]


def _collect_offers(category_dict) -> Iterator[RawOffer]:
    logger.info("Requesting offers of category %s", category_dict.get('category_name'))

    response = requests.get(category_dict.get('category_url'))

    if not response.ok:
        logger.warn("Status code %s: %s", response.status_code, response.text)
        return

    soup = BeautifulSoup(response.text, 'html5lib')
    div_table_offers = soup.find('div', class_='innertCnt')
    table_rows = div_table_offers.find_all('tr')

    try:
        screenshot = make_screenshot_from_html(response.text, category_dict.get('category_url'))
    except Exception:
        logger.exception("Screenshot failed")
        screenshot = None

    for tr in table_rows:
        last_td = tr.findChildren('td', recursive=False)[-1]
        last_td_text = last_td.text.replace(' ', '')

        try:
            Decimal(last_td_text)
        except InvalidOperation:
            logger.warn('This row does not contain offer')
            continue

        yield RawOffer(
            name=tr.findChildren('td', recursive=False)[0].text.strip(),
            measure_unit=category_dict.get('measure_unit'),
            price_with_vat=Decimal(last_td_text),
            price_without_vat=Decimal(tr.findChildren('td', recursive=False)[-2].text.replace(' ', '')),
            delivery_cost=category_dict.get('delivery_cost'),
            extraction_date=timezone.now(),
            page_url=category_dict.get('category_url'),
            image_url=None,
            screenshot_pdf_url=screenshot.url if screenshot else None,
        )


def parse_offers() -> Iterator[RawOffer]:
    logger.info('Parsing offers start')

    for category in CATEGORIES:
        yield from _collect_offers(category)

    logger.info('Parsing offers finished')
