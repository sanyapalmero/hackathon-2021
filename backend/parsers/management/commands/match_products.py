from django.core.management import BaseCommand

from ...models import Offer, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        offers = Offer.objects.all()
        for offer in offers:
            if "plity-perekrytij" in offer.page_url:
                product_id = 931
            elif "bloki-betonnye-dlya-sten-podvalov-fbs" in offer.page_url:
                product_id = 965
            elif "trubniy-prokat" in offer.page_url:
                product_id = 940
            elif "armatura" in offer.page_url:
                product_id = 1024
            elif "ПК" in offer.name:
                product_id = 931
            elif "ПБ" in offer.name or "СПТК" in offer.name or "ПТВ" in offer.name or "ПТК" in offer.name or "ППС" in offer.name:
                product_id = 931
            elif "ПТ" in offer.name or "ПД" in offer.name or "НВ" in offer.name or "7Пб" in offer.name or "ПО" in offer.name or "П " in offer.name:
                product_id = 931
            elif "ФБС" in offer.name or "ФБ 1" in offer.name or "БФ" in offer.name:
                product_id = 965
            else:
                product_id = None

            if product_id:
                product = Product.objects.get(pk=product_id)
                offer.product = product
                offer.save()
