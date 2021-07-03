import django_filters
from django_filters.rest_framework import FilterSet


class ProductFilterSet(FilterSet):
    name = django_filters.CharFilter()
    name__contains = django_filters.CharFilter(field_name='name', lookup_expr='contains')

    offer__name = django_filters.CharFilter(field_name='offer__name')
    offet__name__contains = django_filters.CharFilter(field_name='offer__name', lookup_expr='contains')

    resource_code = django_filters.CharFilter(field_name='offer__resource_code')
