from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Product, Offer, OfferPrice
from .serializers import ProductListSerializer, OfferDetailSerializer, ProductDetailSerializer, OfferPriceSerializer, \
    OfferApproveSerializer, OfferPriceApproveSerializer, OfferExcelSerializer
from .filters import ProductFilterSet, OfferFilterSet, OfferPriceFilterSet, OfferExcelFilterSet


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


class ExcelOffersViewSet(GenericAPIView):
    serializer_class = OfferExcelSerializer
    permission_classes = [IsAuthenticated, ]
    filterset_class = OfferExcelFilterSet

    def get(self, request, *args, **kwargs):
        pass


class OfferViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Offer.objects.all().prefetch_related('prices')
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated, ]
    filterset_class = OfferFilterSet

    serializers_mapping = {
        'list': OfferDetailSerializer,
        'retrieve': OfferDetailSerializer,
        'approve': OfferApproveSerializer,
    }

    def get_serializer_class(self):
        return self.serializers_mapping.get(self.action, self.serializer_class)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsAdminUser],
        url_path='approve',
    )
    def approve(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.approve()

        return Response(status=status.HTTP_200_OK)



class OfferPriceViewSet(ListModelMixin, GenericViewSet):
    queryset = OfferPrice.objects.all()
    serializer_class = OfferPriceSerializer
    permission_classes = [IsAuthenticated, ]
    filter_class = OfferPriceFilterSet

    serializers_mapping = {
        'list': OfferPriceSerializer,
        'approve': OfferPriceApproveSerializer,
    }

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsAdminUser],
        url_path='approve',
    )
    def approve(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.approve()

        return Response(status=status.HTTP_200_OK)