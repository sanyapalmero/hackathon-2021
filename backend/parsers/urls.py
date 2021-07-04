from django.urls import path

from . import views

app_name = "parsers"

urlpatterns = [
    path("", views.ProductsView.as_view(), name="updates"),
    path("product/<int:pk>/", views.ProductView.as_view(), name="product"),
    path('search-offers/', views.SearchOfferView.as_view(), name='search-offers'),
    path("offer/<int:pk>/", views.OfferView.as_view(), name="offer"),
    path("manage-updates/", views.ManageUpdatesView.as_view(), name="manage-updates"),
    path("manage-updates/accept/<int:pk>/", views.AcceptUpdateView.as_view(), name="accept-update"),
    path("manage-updates/decline/<int:pk>/", views.DeclineUpdateView.as_view(), name="decline-update"),
]
