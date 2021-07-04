from django.urls import path

from . import views

app_name = "parsers"

urlpatterns = [
    path("", views.ProductsView.as_view(), name="products"),
    path("product/<int:pk>/", views.ProductView.as_view(), name="product"),
    path("offer/<int:pk>/", views.OfferView.as_view(), name="offer"),
]
