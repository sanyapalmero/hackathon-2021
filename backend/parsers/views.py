from django.core.paginator import Paginator
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
        offers = Paginator(offers, self.offers_per_page).get_page(self.request.GET.get('page'))
        context["offers"] = offers

        return context
