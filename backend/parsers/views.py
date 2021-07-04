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
from .filters import ProductFilterSet, OfferFilterSet, OfferPriceFilterSet
from .services.excel_report import OfferExcelReport


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
    queryset = Offer.objects.all().select_related('product', 'product').prefetch_related('prices')
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated, ]
    filterset_class = OfferFilterSet

    serializers_mapping = {
        'list': OfferDetailSerializer,
        'retrieve': OfferDetailSerializer,
        'approve': OfferApproveSerializer,
        'excel': OfferExcelSerializer,
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

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, IsAdminUser],
        url_path='excel',
    )
    def excel(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        reporter = OfferExcelReport()
        report = reporter.generate(queryset)

        return Response({'link': report.excel.url}, status=status.HTTP_200_OK)



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