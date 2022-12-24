# from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.contrib import messages
from my_user.daily_tasks import My_Send_Email
from django.template.loader import render_to_string

from niser_app.local_settings import *

from .forms import *
from .models import *

def index(request): 
    items = Listing.objects.filter(sold = False)
    return render(request, 'listings/index.html', {'items': items})

def submit(request):
    if request.user is None or not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to submit a listing.')
        return redirect('/listings')
    
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user.profile
            listing.created = now()
            listing.save()

            My_Send_Email(
                to=[request.user.email],
                subject='New Listing Submitted',
                message=render_to_string("listings/list_feedback.txt", {"DOMAIN": DOMAIN, "name": request.user.name, "id": listing.id}),
            ).start()
            
            return redirect('/listings')
    else:
        form = ListingForm()
    return render(request, 'listings/submit.html', {'form': form})

class ListingDetail(DetailView):
    model = Listing
    template_name = 'listings/listing.html'

# def search(request):
#     if request.method == 'GET':
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             search_string = form.cleaned_data['query']

#             words = search_string.lower().split(' ')
#             vector = SearchVector('title', 'category__name', 'location__location', 
#                     'condition__condition', 'description', 'op')

#             query = SearchQuery(words[0])
#             for word in words[1:]:
#                 query = query | SearchQuery(word)

#             sort_by = form.cleaned_data['sort_by']
#             sort_by = ('-rank',) if sort_by == '-rank' else ('-rank', sort_by)
#             listings = Listing.objects.annotate(rank=SearchRank(vector,
#                 query)).order_by(*sort_by)

#             return render(request, 'results.html',
#                     {'search_string': search_string, 'listings': listings})

#     return HttpResponseRedirect('/')
