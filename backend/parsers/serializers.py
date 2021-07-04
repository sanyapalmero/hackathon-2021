from .models import Product, Provider, OfferPrice, Offer

from django.db import models
from rest_framework import serializers


class CustomChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class OfferPriceSerializer(serializers.ModelSerializer):
    status = CustomChoiceField(choices=OfferPrice.Status.choices)

    class Meta:
        model = OfferPrice
        fields = '__all__'


class OfferPriceApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferPrice
        fields = ('id',)

    def approve(self):
        self.instance.state = Offer.Status.PUBLISHED.value
        self.instance.save(update_fields=('state',))


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
    status = CustomChoiceField(choices=Offer.Status.choices)

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
        )


class OfferExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ()


    def excel(self, query):
        pass

class OfferApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = (
            'id',
        )

    def approve(self):
        self.instance.state = Offer.Status.PUBLISHED.value
        self.instance.save(update_fields=('state',))   


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

    class Meta:
        model = Product
        fields = ('id', 'name', 'measure_unit', 'resource_code', 'avg_offer_price', 'min_offer_price')


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

