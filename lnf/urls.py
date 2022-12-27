from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from .views import *

urlpatterns = [
    path('', all_items, name = 'lnf'),
    path('found/', found_items, name = 'lnf-found'),
    path('lost/', lost_items, name = 'lnf-lost'),
    path('item/<int:pk>', item_view, name = 'lnf-item'),
    path('add/', submit_view, name = 'lnf-add'),
    path('search/', search, name = 'lnf-search'),
    path('return_request/<int:pk>', return_request, name = 'lnf-return_request'),
    path('mark_claimed/<int:pk>', mark_claimed, name = 'lnf-mark_claimed'),
]# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
