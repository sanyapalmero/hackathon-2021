from django_filters.rest_framework import FilterSet

from . import models


class ProductFilterSet(FilterSet):
    class Meta:
        model = models.Product
        fields = {
            'name': ['exact', 'icontains'],
            'offers__name': ['exact', 'icontains'],
            'resource_code': ['exact', 'icontains'],
        }


class OfferFilterSet(FilterSet):
    class Meta:
        model = models.Offer
        fields = {
            'product__id': ['exact'],
            'status': ['exact']
        }


class OfferExcelFilterSet(FilterSet):
    class Meta:
        model = models.Offer
        fields = '__all__'

    @classmethod
    def get_fields(cls):
        fields = super().get_fields()
        for field_name in fields.copy():
            lookup_list = cls.Meta.model._meta.get_field(field_name).get_lookups().keys()
            fields[field_name] = lookup_list
        return fields


class OfferPriceFilterSet(FilterSet):
    class Meta:
        model = models.OfferPrice
        fields = {
            'offer__id': ['exact'],
            'offer__product__id': ['exact'],
            'status': ['exact'],
            'extraction_date': ['exact', 'lte', 'gte', 'gt', 'lt']
        }