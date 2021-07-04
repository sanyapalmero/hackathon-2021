from django.core.paginator import Paginator
from django.db import models
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import generic
from users.decorators import admin_required, login_required

from .forms import OfferFilterForm
from .models import Offer, OfferPrice, Product
from .services.excel_report import OfferExcelReport


class ProductsView(generic.ListView):
    template_name = 'parsers/updates.html'
    model = Product
    paginate_by = 20

    def get_queryset(self):
        products_qs = super(ProductsView, self).get_queryset()
        products_qs = products_qs.annotate(
            last_updated=models.Min("offer__last_updated", filter=models.Q(offer__status=Offer.Status.PUBLISHED)),
        ).exclude(last_updated__isnull=True).order_by("last_updated")

        return products_qs


@method_decorator(login_required, name="dispatch")
class ProductView(generic.DetailView):
    model = Product
    template_name = "parsers/product.html"
    context_object_name = "product"
    offers_per_page = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        offers = self.object.offer_set\
            .filter(status=Offer.Status.PUBLISHED)\
            .annotate_price_with_vat()\
            .filter(price_with_vat__isnull=False)\
            .order_by("price_with_vat")
        offers_page = Paginator(offers, self.offers_per_page).get_page(self.request.GET.get('page'))
        context["offers"] = offers_page

        aggr = offers.aggregate(
            min_price=models.Min("price_with_vat"),
            avg_price=models.Avg("price_with_vat"),
        )
        context["min_price"] = aggr["min_price"]
        context["avg_price"] = aggr["avg_price"]

        now = timezone.now()

        prices_graph = []
        for step in range(12, 1, -1):
            gte_date = (now-timezone.timedelta(days=7*step)).date()
            lte_date = (now-timezone.timedelta(days=7*(step-1))).date()

            ofp_qs = OfferPrice.objects.filter(offer__in=offers,
                                               extraction_date__date__gte=gte_date,
                                               extraction_date__date__lte=lte_date)
            aggr = ofp_qs.aggregate(avg_price=models.Avg("price_with_vat"))
            if aggr['avg_price']:
                prices_graph.append((str(aggr['avg_price']), gte_date.isoformat()))

        context['product_price_range'] = prices_graph

        return context


@method_decorator(login_required, name="dispatch")
class SearchOfferView(generic.ListView):
    template_name_suffix = '-search'
    model = Offer
    paginate_by = 30
    form_class = OfferFilterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        return context

    def _get_excel(self, request, qs):
        excel_file = OfferExcelReport(
            sheet_name='Отчет на {}'.format(timezone.now().strftime('%d.%m.%Y'))
        )
        excel_file.generate(qs=qs)

        response = HttpResponse(
            excel_file.for_http_response(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % excel_file.filename
        return response

    def get(self, request):
        form = self.form_class(request.GET)

        if form.is_valid():
            excel = form.cleaned_data['excel']
            if excel:
                return self._get_excel(request=request, qs=self.get_queryset())

        return super().get(request)

    def get_queryset(self):
        qs = self.model.objects.filter(status=self.model.Status.PUBLISHED)

        search_offers_str = self.request.GET.get('search_offers_str')

        query = (
            Q(name__icontains=search_offers_str) |
            Q(provider__name__icontains=search_offers_str) |
            Q(product__name__icontains=search_offers_str)
        )

        if search_offers_str:
            qs = qs.filter(query)

        form = self.form_class(self.request.GET)

        if form.is_valid():
            name = form.cleaned_data['name']
            if name:
                qs = qs.filter(name__icontains=name)

            provider = form.cleaned_data['provider']
            if provider:
                qs = qs.filter(provider=provider)

            date_start = form.cleaned_data['date_start']
            if date_start:
                qs = qs.filter(last_updated__gte=date_start)

            date_end = form.cleaned_data['date_end']
            if date_end:
                qs = qs.filter(last_updated__lte=date_end)
        return qs


@method_decorator(login_required, name="dispatch")
class OfferView(generic.DetailView):
    model = Offer
    template_name = "parsers/offer.html"

    def get_context_data(self, **kwargs):
        context = super(OfferView, self).get_context_data(**kwargs)

        now = timezone.now()

        prices_graph = []
        for step in range(12, 1, -1):
            gte_date = (now - timezone.timedelta(days=7 * step)).date()
            lte_date = (now - timezone.timedelta(days=7 * (step - 1))).date()

            ofp_qs = self.object.offerprice_set.filter(
                extraction_date__date__gte=gte_date,
                extraction_date__date__lte=lte_date)
            aggr = ofp_qs.aggregate(avg_price=models.Avg("price_with_vat"))
            if aggr['avg_price']:
                prices_graph.append((str(aggr['avg_price']), gte_date.isoformat()))

        context['product_price_range'] = prices_graph
        return context


@method_decorator(admin_required, name="dispatch")
class ManageUpdatesView(generic.ListView):
    model = Offer
    template_name = "parsers/manage-updates.html"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()

        updated_qs = qs.filter(status=Offer.Status.PUBLISHED).filter(offerprice__status=OfferPrice.Status.WAITING)
        new_qs = qs.filter(status=Offer.Status.WAITING)

        return (updated_qs | new_qs).distinct()


@method_decorator(admin_required, name="dispatch")
class AcceptUpdateView(generic.View):
    def post(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        offer.status = Offer.Status.PUBLISHED
        offer.save()

        last_waiting_offer_price = offer.last_waiting_offer_price
        if last_waiting_offer_price:
            last_waiting_offer_price.status = OfferPrice.Status.PUBLISHED
            last_waiting_offer_price.save()

        return redirect("parsers:manage-updates")


@method_decorator(admin_required, name="dispatch")
class DeclineUpdateView(generic.View):
    def post(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        if offer.is_waiting:
            offer.status = Offer.Status.UNPUBLISHED
            offer.save()

        last_waiting_offer_price = offer.last_waiting_offer_price
        if last_waiting_offer_price:
            last_waiting_offer_price.status = OfferPrice.Status.UNPUBLISHED
            last_waiting_offer_price.save()

        return redirect("parsers:manage-updates")
