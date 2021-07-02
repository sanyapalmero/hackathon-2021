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
    last_updated = models.DateField(null=True, blank=False, verbose_name="Дата последнего обновления")
    page_url = models.URLField(null=True, blank=False, verbose_name="Ссылка на страницу")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name="Поставщик")
    image_url = models.URLField(null=True, blank=False, verbose_name="Ссылка на картинку")
    status = models.IntegerField(choices=Status.choices, db_index=True, verbose_name='статус')
