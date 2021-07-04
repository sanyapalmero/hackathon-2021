import hashlib
import os

from django.db import models
from django.urls import reverse
from django.utils import timezone


class Product(models.Model):
    """
    Модель: Товар
    """

    name = models.CharField(max_length=255, verbose_name="Наименование")
    measure_unit = models.CharField(null=True, blank=True, max_length=255, verbose_name="Единица измерения")
    resource_code = models.CharField(null=True, blank=True, max_length=255, verbose_name="Код строительного ресурса")

    @property
    def image_url(self):
        offer = self.offer_set.filter(image_url__isnull=False).first()
        return offer.image_url if offer else None


class Provider(models.Model):
    """
    Модель: Поставщик
    """

    name = models.CharField(max_length=255, verbose_name="Наименование")
    inn = models.CharField(max_length=255, verbose_name="ИНН")
    kpp = models.CharField(max_length=255, verbose_name="КПП")
    warehouse_location = models.CharField(max_length=255, verbose_name="Населенный пункт склада")


class OfferQuerySet(models.QuerySet):
    def annotate_price_with_vat(self):
        return self.annotate(price_with_vat=models.Subquery(
            OfferPrice.objects
            .filter(offer_id=models.OuterRef("pk"), status=OfferPrice.Status.PUBLISHED)
            .order_by("-extraction_date")
            .values("price_with_vat")[:1]
        ))


class Offer(models.Model):
    """
    Модель: Предложение
    """

    class Status(models.IntegerChoices):
        UNPUBLISHED = 1, 'Неопубликован'
        WAITING = 2, 'Ожидает подтверждения'
        PUBLISHED = 3, 'Опубликован'

    resource_code = models.CharField(null=True, blank=True, max_length=255, verbose_name="Код строительного ресурса")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    measure_unit = models.CharField(null=True, blank=True, max_length=255, verbose_name="Единица измерения")
    last_updated = models.DateTimeField(verbose_name="Дата последнего обновления")
    page_url = models.URLField(verbose_name="Ссылка на страницу")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name="Поставщик")
    image_url = models.URLField(null=True, blank=True, verbose_name="Ссылка на картинку")
    status = models.IntegerField(choices=Status.choices, db_index=True, verbose_name="Статус")
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Товар")

    objects = OfferQuerySet.as_manager()

    @property
    def last_offer_price(self):
        return OfferPrice.objects\
            .filter(offer=self, status=OfferPrice.Status.PUBLISHED)\
            .order_by("extraction_date")\
            .last()

    @property
    def last_waiting_offer_price(self):
        return OfferPrice.objects\
            .filter(offer=self, status=OfferPrice.Status.WAITING)\
            .order_by("extraction_date")\
            .last()

    def get_absolute_url(self):
        return reverse("parsers:offer", kwargs={"pk": self.pk})

    @property
    def is_waiting(self):
        return self.status == self.Status.WAITING


class OfferPrice(models.Model):
    """
    Модель: Цена предложения в определенный момент времени
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
    extraction_date = models.DateTimeField(verbose_name="Дата извлечения")
    status = models.IntegerField(choices=Status.choices, db_index=True, verbose_name="Статус")
    screenshot_pdf_url = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ссылка на скриншот PDF")


def get_excel_file_path(excel_report, filename):
    filename, ext = os.path.splitext(filename)
    hasher = hashlib.sha1()
    hasher.update((filename + str(timezone.now())).encode('utf-8'))
    return os.path.join('excel-report', hasher.hexdigest() + ext.lower())


class ExcelReport(models.Model):
    excel = models.FileField(upload_to=get_excel_file_path, verbose_name='файл excel')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'отчет excel'
        verbose_name_plural = 'отчеты excel'
        ordering = (
            '-created_at',
        )
