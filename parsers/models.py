from django.db import models


class Provider(models.Model):
    """
    Модель: Поставщик
    """

    name = models.CharField(max_length=255, verbose_name="Наименование")
    inn = models.CharField(max_length=255, verbose_name="ИНН")
    kpp = models.CharField(max_length=255, verbose_name="КПП")
    warehouse_location = models.CharField(max_length=255, verbose_name="Населенный пункт склада")
