from django.shortcuts import render

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product, Offer
from .serializers import ProductListSerializer, OfferDetailSerializer, ProductDetailSerializer
from .filters import ProductFilterSet


class ProductViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Product.objects.all().prefetch_related('offers', 'offers__prices').distinct()
    filterset_class = ProductFilterSet
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated, ]

    serializers_mapping = {
        'list': ProductListSerializer,
        'retrieve': ProductDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializers_mapping.get(self.action, self.serializer_class)


class OffersViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Offer.objects.filter(status=Offer.Status.PUBLISHED.value).prefetch_related('prices')
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated, ]
