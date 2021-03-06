# Generated by Django 3.2.4 on 2021-07-02 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0002_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.IntegerField(choices=[(1, 'Неопубликован'), (2, 'Ожидает подтверждения'), (3, 'Опубликован')], db_index=True, verbose_name='Статус'),
        ),
        migrations.CreateModel(
            name='OfferPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_with_vat', models.CharField(max_length=255, verbose_name='Отпускная цена с НДС')),
                ('price_without_vat', models.CharField(max_length=255, verbose_name='Стоимость доставки')),
                ('delivery_cost', models.CharField(max_length=255, verbose_name='Наименование')),
                ('status', models.IntegerField(choices=[(1, 'Неопубликован'), (2, 'Ожидает подтверждения'), (3, 'Опубликован')], db_index=True, verbose_name='Статус')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsers.offer', verbose_name='Оффер')),
            ],
        ),
    ]
