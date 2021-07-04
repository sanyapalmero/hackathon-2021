import django_filters
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


class OfferPriceFilterSet(FilterSet):
    class Meta:
        model = models.OfferPrice
        fields = {
            'offer__id': ['exact'],
            'offer__product__id': ['exact'],
            'status': ['exact'],
            'extraction_date': ['exact', 'lte', 'gte', 'gt', 'lt']
        }