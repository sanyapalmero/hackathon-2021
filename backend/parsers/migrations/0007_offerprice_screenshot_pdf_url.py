# Generated by Django 3.2.4 on 2021-07-03 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0006_auto_20210702_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerprice',
            name='screenshot_pdf_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка на скриншот PDF'),
        ),
    ]
