from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name = 'listings'),
    path('submit/', submit, name = 'listings-submit'),
    path('listing/<int:pk>', listings_view, name = 'listings-item'),
    path("mark_sold/<int:pk>", mark_sold, name = "listings-mark_sold"),
    path("buy_request/<int:pk>", buy_request, name = "listings-buy_request")
    # path('search/', search, name = 'search'),
]# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
