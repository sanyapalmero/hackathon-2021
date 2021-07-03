# Generated by Django 3.2.4 on 2021-07-03 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0006_auto_20210702_2320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='keywords',
        ),
        migrations.AddField(
            model_name='product',
            name='measure_unit',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Единица измерения'),
        ),
        migrations.AddField(
            model_name='product',
            name='resource_code',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Код строительного ресурса'),
        ),
    ]
