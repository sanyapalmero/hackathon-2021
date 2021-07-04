from .models import Product, Provider, OfferPrice, Offer

from django.db import models
from rest_framework import serializers


class OfferPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferPrice
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    last_offer_price = OfferPriceSerializer()

    class Meta:
        model = Offer
        fields = (
            'id',
            'resource_code',
            'name',
            'measure_unit',
            'last_updated',
            'page_url',
            'provider',
            'image_url',
            'status',
            'product',
            'last_offer_price',
        )


class OfferSerializerWithoutPrice(OfferSerializer):
    class Meta:
        model = Offer
        fields = (
            'id',
            'resource_code',
            'name',
            'measure_unit',
            'last_updated',
            'page_url',
            'provider',
            'image_url',
            'status',
        )


class OfferDetailSerializer(serializers.ModelSerializer):
    prices = OfferPriceSerializer(many=True, source='three_month_price')

    class Meta:
        model = Offer
        fields = (
            'id',
            'resource_code',
            'name',
            'measure_unit',
            'last_updated',
            'page_url',
            'provider',
            'image_url',
            'status',
            'product',
            'prices',
        )


class ProductListSerializer(serializers.ModelSerializer):
    offers_count = serializers.SerializerMethodField()

    def get_offers_count(self, instance):
        return instance.offers.count()

    class Meta:
        model = Product
        fields = ('id', 'name', 'measure_unit', 'resource_code', 'offers_count')


class ProductDetailSerializer(serializers.ModelSerializer):
    avg_offer_price = serializers.SerializerMethodField()
    min_offer_price = serializers.SerializerMethodField()
    offers = OfferSerializerWithoutPrice(many=True)
    prices = serializers.SerializerMethodField()

    def get_avg_offer_price(self, instance):
        return Product.objects.filter(
            id=instance.id,
            offers__prices__status=OfferPrice.Status.PUBLISHED
        ).annotate(
            avg_price=models.Avg('offers__prices__price_with_vat')
        ).values_list('avg_price', flat=True)[0]

    def get_min_offer_price(self, instance):
        return Product.objects.filter(
            id=instance.id,
            offers__prices__status=OfferPrice.Status.PUBLISHED
        ).annotate(
            avg_price=models.Min('offers__prices__price_with_vat')
        ).values_list('avg_price', flat=True)[0]

    def get_prices(self, instance):
        return OfferPriceSerializer(OfferPrice.objects.filter(offer__product_id=instance.id), many=True).data

    class Meta:
        model = Product
        fields = ('id', 'name', 'measure_unit', 'resource_code', 'avg_offer_price', 'min_offer_price', 'offers', 'prices')


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

