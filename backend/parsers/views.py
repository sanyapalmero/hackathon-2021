from django.core.paginator import Paginator
from django.db import models
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views import generic
from users.decorators import login_required

from .forms import OfferFilterForm
from .models import Offer, Product


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

    def get_queryset(self):
        qs = super().get_queryset()

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
