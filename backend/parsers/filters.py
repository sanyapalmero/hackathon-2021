import django_filters
from django_filters.rest_framework import FilterSet


class ProductFilterSet(FilterSet):
    name = django_filters.CharFilter()
    name__icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    offer__name = django_filters.CharFilter(field_name='offer__name')
    offet__name__icontains = django_filters.CharFilter(field_name='offer__name', lookup_expr='icontains')

    resource_code = django_filters.CharFilter(field_name='offer__resource_code')
