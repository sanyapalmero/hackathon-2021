from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views import generic
from users.decorators import login_required

from .models import Offer, Product


class ProductsView(generic.TemplateView):
    template_name = 'parsers/products.html'


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

    def get_queryset(self):
        qs = super().get_queryset()

        search_offers_str = self.request.GET.get('search_offers_str')

        query = (
            Q(name__icontains=search_offers_str) |
            Q(provider__name__icontains=search_offers_str) |
            Q(product__name__icontains=search_offers_str)
        )

        if not search_offers_str:
            return qs

        qs = qs.filter(query)

        return qs


@method_decorator(login_required, name="dispatch")
class OfferView(generic.DetailView):
    model = Offer
    template_name = "parsers/offer.html"
