from django.db import models


class Provider(models.Model):
    """
    Модель: Поставщик
    """

    name = models.CharField(max_length=255, verbose_name="Наименование")
    inn = models.CharField(max_length=255, verbose_name="ИНН")
    kpp = models.CharField(max_length=255, verbose_name="КПП")
    warehouse_location = models.CharField(max_length=255, verbose_name="Населенный пункт склада")


class Offer(models.Model):
    """
    Модель: Предложение
    """

    class Status(models.IntegerChoices):
        UNPUBLISHED = 1, 'Неопубликован'
        WAITING = 2, 'Ожидает подтверждения'
        PUBLISHED = 3, 'Опубликован'

    resource_code = models.CharField(null=True, blank=False, max_length=255, verbose_name="Код строительного ресурса")
    name = models.CharField(null=True, blank=False, max_length=255, verbose_name="Наименование")
    measure_unit = models.CharField(null=True, blank=False, max_length=255, verbose_name="Единица измерения")
    last_updated = models.DateTimeField(null=True, blank=False, verbose_name="Дата последнего обновления")
    page_url = models.URLField(null=True, blank=False, verbose_name="Ссылка на страницу")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name="Поставщик")
    image_url = models.URLField(null=True, blank=False, verbose_name="Ссылка на картинку")
    status = models.IntegerField(choices=Status.choices, db_index=True, verbose_name="Статус")

    @property
    def last_offer_price(self):
        return OfferPrice.objects.filter(offer=self).order_by("extraction_date").last()


class OfferPrice(models.Model):
    """
    Модель: Цена предложегния в определенный момент времени
    """

    class Status(models.IntegerChoices):
        UNPUBLISHED = 1, 'Неопубликован'
        WAITING = 2, 'Ожидает подтверждения'
        PUBLISHED = 3, 'Опубликован'

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, verbose_name="Оффер")
    price_with_vat = models.DecimalField(
        max_length=255, decimal_places=2, max_digits=12, verbose_name="Отпускная цена с НДС"
    )
    price_without_vat = models.DecimalField(
        max_length=255, decimal_places=2, max_digits=12, verbose_name="Отпускная цена без НДС"
    )
    delivery_cost = models.DecimalField(
        max_length=255, decimal_places=2, max_digits=12, verbose_name="Стоимость доставки"
    )
    extraction_date = models.DateTimeField(null=True, blank=False, verbose_name="Дата извлечения")
    status = models.IntegerField(choices=Status.choices, db_index=True, verbose_name="Статус")
