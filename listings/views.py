# from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.shortcuts import render, redirect
from django.contrib import messages
from my_user.daily_tasks import My_Send_Email, My_Send_Notification
from django.template.loader import render_to_string

from niser_app.local_settings import *

from .forms import *
from .models import *


# helper functions

def send_appropriate_notification(listing):  # takes a Listing object

    message = f"{listing.seller.user.name} wants to sell a {listing}."
    title = "NISER Listings"
    image = DOMAIN+listing.photo.url if listing.photo else None
    
    My_Send_Notification(
        message=message,
        title=title,
        image=image
    ).start()


# Create your views here.


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
            
            send_appropriate_notification(listing)
            
            return redirect('/listings')
    else:
        form = ListingForm()
    return render(request, 'listings/submit.html', {'form': form})
    
def listings_view(request, pk):
    listing = Listing.objects.get(pk=pk)
    return render(request, 'listings/listing.html', {'listing':listing, "user":request.user if request.user!=None or request.user.is_authenticated else None})

def mark_sold(request, pk):
    listing = Listing.objects.get(pk=pk)
    if listing.sold:
        messages.error(request, 'Listing already marked as sold.')
        return redirect('/listings')
    if request.user.is_authenticated:
        if listing.seller == request.user.profile:
            listing.sold = True
            listing.save()
            messages.success(request, 'Listing marked as sold')
            My_Send_Email(
                to=[listing.seller.user.email],
                subject='Listing marked Sold',
                message=render_to_string("listings/marked_sold_email.txt", {"DOMAIN": DOMAIN, "user": request.user, "listing": listing})
            ).start()
            return redirect('/listings')
    messages.error(request, 'Only the person who submitted the listing can mark it as sold.')
    return redirect('/listings')

def buy_request(request, pk):
    if request.user.is_authenticated:
        listing = Listing.objects.get(pk=pk)
        if listing.seller != request.user.profile:
            My_Send_Email(
                to = [listing.seller.user.email],
                message=render_to_string("listings/buy_request.txt", {"seller": listing.seller.user.name, "buyer": request.user.name, "listing": listing, "DOMAIN": DOMAIN}),
                subject= f"Buy Request for your listing: {listing}",
                cc = [request.user.email]
            ).start()
            messages.success(request, 'Request sent.')
        else:
            messages.error(request, 'You cannot send a buy request to yourself.')
    else:
        messages.error(request, 'Login to send a buy requests')
    return redirect('/listings')


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
#                     {'search_string': search_string, 'listings': [listing for listing in listings if not listing.sold]})

#     return HttpResponseRedirect('/')
