from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

import parsers.views

router = DefaultRouter()

router.register(r'products', parsers.views.ProductViewSet)
router.register(r'offers', parsers.views.OffersViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path("auth/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns = (
        static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        )
        + urlpatterns
    )
