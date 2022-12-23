from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name = 'listings'),
    path('submit/', submit, name = 'listings-submit'),
    path('listing/<int:pk>', ListingDetail.as_view(), name = 'listings-item'),
    # path('search/', search, name = 'search'),
]# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
