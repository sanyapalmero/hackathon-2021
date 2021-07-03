import logging
import re
import time
from decimal import Decimal
from typing import Iterator, Optional

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from .raw_offer import RawOffer
from .screenshot import make_screenshot_from_html

logger = logging.getLogger(__name__)


BASE_URL = "https://orenburg.spk.ru"
SELECTED_CATEGORIES_FOR_PARSING = [
    "https://orenburg.spk.ru/catalog/metalloprokat/trubniy-prokat/truba-profilnaya/",
    "https://orenburg.spk.ru/catalog/metalloprokat/sortovoy-prokat/armatura/"
]

PAUSE = 0.2


def _get_pages_count(soup: BeautifulSoup) -> int:
    """
    Получает страницу товаров, находит пагинатор и возвращает общее число страниц
    """

    last_page_link = soup.find("a", attrs={"class": "pager__last"})
    last_page_url = last_page_link.get("href")
    return int(last_page_url.split("=")[1])


def _parse_product(soup: BeautifulSoup) -> Optional[RawOffer]:
    """
    Открывает страницу продукта и парсит данные товара
    """

    title_link = soup.find("a", attrs={"class": "product-card__title-link"})
    product_url = BASE_URL + title_link.get("href")
    logger.info("Openning product page: %s", product_url)
    product_page = requests.get(product_url)
    if product_page.status_code != 200:
        logger.warn("Status code %s: %s", product_page.status_code, product_page.text)
        return

    parsed_product_page = BeautifulSoup(product_page.content, "html5lib")

    product_title_h1 = parsed_product_page.find("h1", attrs={"itemprop": "name"})
    if product_title_h1.text:
        name = product_title_h1.text.lstrip().rstrip()
    else:
        logger.warn("No product name")
        return None

    product_price_div = parsed_product_page.find("div", attrs={
        "data-role": "unit",
        "data-type": "base",
        "class": "product-multiple__price-item",
    })

    if product_price_div.text:
        product_price_text = re.sub(r"\s+", "", product_price_div.text)

        if product_price_text != "Цена по запросу":
            splitted_price = product_price_text.split("/")
            if len(splitted_price) == 2:
                meausure_unit = product_price_text.split("/")[1]
                price_with_vat = product_price_text.split("/")[0].replace("руб.", "")
                price_with_vat = Decimal(price_with_vat.replace(",", "."))

                price_without_vat = price_with_vat - (price_with_vat * Decimal("0.16"))
            else:
                logger.warn("Splitted price has more than two elements")
                return None
        else:
            logger.warn("Product price needs request")
            return None
    else:
        logger.warn("No product price")
        return None

    # Ссылка на прайслист доставки: https://orenburg.spk.ru/pricelist/1028/
    # Выбрана минимальная цена для третьей зоны Оренбурга
    delivery_cost = Decimal("1600")

    image = parsed_product_page.find("img", attrs={"class": "photo-slider__item"})
    image_url = image.get("src") if image else None

    logger.info(
        "New offer was successfully parsed: %s | %s | %s | %s | %s | %s | %s | %s",
        name,
        meausure_unit,
        price_with_vat,
        price_without_vat,
        delivery_cost,
        timezone.now(),
        product_url,
        BASE_URL + image_url
    )

    try:
        screenshot = make_screenshot_from_html(product_page.text, product_url)
    except Exception:
        logger.exception("Screenshot failed")
        screenshot = None

    return RawOffer(
        name=name,
        measure_unit=meausure_unit,
        price_with_vat=price_with_vat,
        price_without_vat=price_without_vat,
        delivery_cost=delivery_cost,
        extraction_date=timezone.now(),
        page_url=product_url,
        image_url=BASE_URL + image_url,
        screenshot_pdf_url=screenshot.url if screenshot else None,
    )


def _get_offer(category_url: str) -> Iterator[RawOffer]:
    """
    Парсит страницу со списком товаров
    """

    logger.info("GET: %s", category_url)
    time.sleep(PAUSE)
    products_page = requests.get(category_url)
    if products_page.status_code != 200:
        logger.warn("Status code %s: %s", products_page.status_code, products_page.text)
        return

    soup = BeautifulSoup(products_page.content, "html5lib")
    pages_count = _get_pages_count(soup)
    logger.info("Total pages: %d", pages_count)

    for page in range(1, pages_count):
        logger.info("Start parsing page %s", page)
        logger.info("GET: %s", category_url + '?page=' + str(page))
        current_page = requests.get(category_url, params={"page": page})
        if current_page.status_code != 200:
            logger.warn("Status code %s: %s", current_page.status_code, current_page.text)
            return

        parsed_page = BeautifulSoup(current_page.content, "html5lib")
        products = parsed_page.find_all("div", attrs={"class": "product-card__wrap card-card-simplified-view"})

        for product in products:
            yield _parse_product(product)


def parse_offers() -> Iterator[RawOffer]:
    offers_count = 0

    logger.info("Start parsing orenburg.spk.ru")

    for category_url in SELECTED_CATEGORIES_FOR_PARSING:
        for offer in _get_offer(category_url):
            if offer:
                offers_count += 1
                yield offer

    logger.info("Parsed %s offers", offers_count)
