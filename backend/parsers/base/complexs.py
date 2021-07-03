import decimal
import logging
import time
from decimal import Decimal
from typing import Iterator, Optional

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from ..base.raw_offer import RawOffer

logger = logging.getLogger(__name__)

PAUSE = 0.2


def _collect_category_offer_urls(category_id: str) -> Iterator[str]:
    logger.info("Requesting subtree of category %s", category_id)

    time.sleep(PAUSE)
    resp = requests.post(
        "https://www.complexs.ru/jbi/update_tree",
        headers={
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "pragma": "no-cache",
            "x-requested-with": "XMLHttpRequest",
            "referrer": "https://www.complexs.ru/jbi",
        },
        data={"id": category_id},
        verify=False,
    )
    if resp.status_code != 200:
        logger.warn("Status code %s: %s", resp.status_code, resp.text)
        return

    resp_json = resp.json()
    if resp_json.get("error"):
        logger.warn("API error: %s", resp.status_code, resp.text)
        return

    items_html = resp_json.get("content", "")
    soup = BeautifulSoup(items_html, 'html5lib')

    for offer_element in soup.select(".file"):
        offer_link = offer_element.select_one("a[href]")
        if offer_link:
            offer_url = "https://www.complexs.ru" + offer_link["href"]
            logger.info("Found offer %s in category %s", offer_url, category_id)
            yield offer_url

    for subcat_element in soup.select(".folder"):
        subcat_link = subcat_element.select_one("a[id]")
        if subcat_link:
            subcat_id = subcat_link["id"]
            logger.info("Found subcategory %s in category %s", subcat_id, category_id)
            yield from _collect_category_offer_urls(subcat_id)


def _collect_all_offer_urls() -> Iterator[str]:
    root_categories = [
        "elem-172973",  # Плиты перекрытий (ПТ) и днища (ПД) каналов
        "elem-159215",  # Плиты перекрытий железобетонные многопустотные
        "elem-156844",  # Плиты перекрытия лотков
        "elem-135286",  # ФБС (сплошные)
    ]

    for category_id in root_categories:
        yield from _collect_category_offer_urls(category_id)


def _get_offer(offer_url) -> Optional[RawOffer]:
    logger.info("Requesting offer %s", offer_url)

    time.sleep(PAUSE)
    resp = requests.get(
        offer_url,
        headers={
            "accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            ),
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "upgrade-insecure-requests": "1",
            "referrer": "https://www.complexs.ru/jbi",
        },
        verify=False,
    )
    if resp.status_code != 200:
        logger.warn("Status code %s: %s", resp.status_code, resp.text)
        return

    soup = BeautifulSoup(resp.text, 'html5lib')

    h1 = soup.select_one("h1")
    name = h1.text if h1 else None
    if not name:
        logger.warn("No h1")
        return None

    price_element = soup.select_one(".pr_basket")
    if not price_element:
        logger.warn("No .pr_basket")
        return None

    price_text = price_element.text.strip().rstrip("руб.").replace(" ", "")
    try:
        price_with_vat = Decimal(price_text)
    except decimal.InvalidOperation:
        logger.warn("Invalid price: %s", price_text)
        return None

    price_without_vat = round(Decimal(float(price_with_vat) * 0.833), 2)

    image_element = soup.select_one("img.img_jbi_src[src]")
    if image_element:
        image_url = "https://www.complexs.ru" + image_element["src"]
    else:
        image_url = None

    return RawOffer(
        name=name,
        measure_unit="шт",
        price_with_vat=price_with_vat,
        price_without_vat=price_without_vat,
        delivery_cost=1300,  # неизвестно
        extraction_date=timezone.now(),
        page_url=offer_url,
        image_url=image_url,
    )


def parse_offers() -> Iterator[RawOffer]:
    offer_count = 0
    for offer_url in _collect_all_offer_urls():
        offer = _get_offer(offer_url)
        if offer:
            offer_count += 1
            yield offer

    logger.info("Parsed %s offers", offer_count)
