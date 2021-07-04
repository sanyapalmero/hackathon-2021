from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Product, Offer, OfferPrice
from .serializers import ProductListSerializer, OfferDetailSerializer, ProductDetailSerializer, OfferPriceSerializer
from .filters import ProductFilterSet, OfferFilterSet, OfferPriceFilterSet


class ProductViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Product.objects.all().prefetch_related('offers', 'offers__prices').order_by('name').distinct()
    filterset_class = ProductFilterSet
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated, ]

    serializers_mapping = {
        'list': ProductListSerializer,
        'retrieve': ProductDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializers_mapping.get(self.action, self.serializer_class)


class OfferViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Offer.objects.filter(status=Offer.Status.PUBLISHED.value).prefetch_related('prices')
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated, ]
    filterset_class = OfferFilterSet


class OfferPriceViewSet(ListModelMixin, GenericViewSet):
    queryset = OfferPrice.objects.filter(status=OfferPrice.Status.PUBLISHED.value)
    serializer_class = OfferPriceSerializer
    permission_classes = [IsAuthenticated, ]
    filter_class = OfferPriceFilterSet