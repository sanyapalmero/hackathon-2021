from django.urls import path

from . import views

app_name = "parsers"

urlpatterns = [
    path("", views.ProductsView.as_view(), name="products"),
]
