from django.core.management import BaseCommand
from django.utils import timezone

from ...base import complexs
from ...base.raw_offer import RawOffer
from ...models import Offer, OfferPrice, Provider


class Command(BaseCommand):
    def find_offer(self, provider: Provider, raw_offer: RawOffer) -> Offer:
        offer = Offer.objects.filter(page_url=raw_offer.page_url, name=raw_offer.name).first()
        if not offer:
            offer = Offer(
                page_url=raw_offer.page_url,
                name=raw_offer.name,
                status=Offer.Status.WAITING,
            )

        offer.provider = provider
        offer.measure_unit = raw_offer.measure_unit
        offer.image_url = raw_offer.image_url
        offer.last_updated = timezone.now()
        offer.save()

        return offer

    def update_offer_price(self, offer: Offer, raw_offer: RawOffer):
        last_offer_price = offer.offerprice_set.order_by("extraction_date").last()
        if not last_offer_price:
            OfferPrice.objects.create(
                offer=offer,
                price_with_vat=raw_offer.price_with_vat,
                price_without_vat=raw_offer.price_without_vat,
                delivery_cost=raw_offer.delivery_cost,
                extraction_date=timezone.now(),
                status=OfferPrice.Status.WAITING,
                screenshot_pdf_url=raw_offer.screenshot_pdf_url,
            )
            return

        all_prices_equal = (
            last_offer_price.price_with_vat == raw_offer.price_with_vat and
            last_offer_price.price_without_vat == raw_offer.price_without_vat and
            last_offer_price.delivery_cost == raw_offer.delivery_cost
        )
        if all_prices_equal:
            last_offer_price.extraction_date = timezone.now()
            last_offer_price.screenshot_pdf_url = raw_offer.screenshot_pdf_url
            last_offer_price.save()
            return

        OfferPrice.objects.create(
            offer=offer,
            price_with_vat=raw_offer.price_with_vat,
            price_without_vat=raw_offer.price_without_vat,
            delivery_cost=raw_offer.delivery_cost,
            extraction_date=timezone.now(),
            status=OfferPrice.Status.WAITING,
            screenshot_pdf_url=raw_offer.screenshot_pdf_url,
        )

    def handle(self, *args, **options):
        parsers = [
            ("complexs.ru", complexs.parse_offers, Provider.objects.get(id=2)),
        ]

        for site_name, parse, provider in parsers:
            self.stdout.write(f"Running {site_name} parser")

            for raw_offer in parse():
                offer = self.find_offer(provider, raw_offer)
                self.update_offer_price(offer, raw_offer)
