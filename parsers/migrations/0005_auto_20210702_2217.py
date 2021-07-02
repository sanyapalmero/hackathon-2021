# Generated by Django 3.2.4 on 2021-07-02 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0004_auto_20210702_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='image_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на картинку'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='last_updated',
            field=models.DateTimeField(verbose_name='Дата последнего обновления'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='measure_unit',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Единица измерения'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='page_url',
            field=models.URLField(verbose_name='Ссылка на страницу'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='resource_code',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Код строительного ресурса'),
        ),
        migrations.AlterField(
            model_name='offerprice',
            name='extraction_date',
            field=models.DateTimeField(verbose_name='Дата извлечения'),
        ),
    ]
