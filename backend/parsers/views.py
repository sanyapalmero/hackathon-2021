from django.views import generic 


class ProductsView(generic.TemplateView):
    template_name = 'parsers/products.html'
