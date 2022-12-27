from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.template.loader import render_to_string

from my_user.daily_tasks import My_Send_Email
from niser_app.local_settings import DOMAIN

from .forms import *
from .models import *

# Create your views here.

def all_items(request):
    items = Item.objects.filter(claimed = False)
    return render(request, 'lnf/index.html', {'kind': 'Recently Added', 'items': items})

def lost_items(request):
    items = Item.objects.filter(kind = 'Lost', claimed = False)
    return render(request, 'lnf/index.html', {'kind': 'Lost', 'items': items})

def found_items(request):
    items = Item.objects.filter(kind = 'Found', claimed = False)
    return render(request, 'lnf/index.html', {'kind': 'Found', 'items': items})

# class ItemDetail(DetailView):
#     model = Item
#     template_name = 'lnf/item.html'
    
    
    
def item_view(request, pk):
    item = Item.objects.get(pk=pk)
    kind = str(item.kind)
    return render(request, 'lnf/item.html', {'item':item, "kind":kind, "user":request.user if request.user!=None or request.user.is_authenticated else None})

def mark_claimed(request, pk):
    item = Item.objects.get(pk=pk)
    
    verb = "Found" if item.kind == "Lost" else "Claimed"
    
    if item.claimed:
        messages.error(request, f'Item already marked as {verb}.')
        return redirect('/lnf')
    if request.user.is_authenticated:
        if item.submitter == request.user.profile:
            item.claimed = True
            item.save()
            messages.success(request, f'Item marked as {verb}')
            My_Send_Email(
                to=[item.submitter.user.email],
                subject=f'Item marked {verb}',
                message=render_to_string("lnf/marked_claimed_email.txt", {"DOMAIN": DOMAIN, "user": request.user, "item": item, "verb": verb})
            ).start()
            return redirect('/lnf')
    messages.error(request, f'Only the person who submitted the item can mark it as {verb}.')
    return redirect('/lnf')

def return_request(request, pk):
    if request.user.is_authenticated:
        item = Item.objects.get(pk=pk)
        if item.submitter != request.user.profile:
            if item.kind == "Lost":
                subject = f"Your {item.category} was found!"
                message = f"{request.user.name} claims to have found your {item}."
            else:
                subject = f"The {item.category} you found was claimed!"
                message = f"{request.user.name} claims to have lost the {item} you have found."
            My_Send_Email(
                to = [item.submitter.user.email],
                message=render_to_string("lnf/return_request.txt", {"to": item.submitter.user.name, "message": message, "item": item, "DOMAIN": DOMAIN}),
                subject= subject,
                cc = [request.user.email]
            ).start()
            messages.success(request, 'Request sent.')
        else:
            messages.error(request, 'You cannot send a return request to yourself.')
    else:
        messages.error(request, 'Login to send a return requests')
    return redirect('/lnf')

def submit_view(request):
    if not request.user or not request.user.is_authenticated:
        messages.error(request, "You must be logged in to submit an item in Lost and Found")
        return redirect("/auth/login")

    if request.method == 'GET':
        form = ItemForm
        return render(request, 'lnf/submit.html', {'form': form})
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.submitter = request.user.profile
            item.save()
            messages.success(request, "Your item has been submitted successfully")
            return redirect('/lnf')
        else:
            return render(request, 'lnf/submit.html', {'form': form})
    

def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_string = form.cleaned_data['keyword']
            words = search_string.lower().split(' ')
            vector = SearchVector('kind', 'location', 'category', 'desc', 'submitter')
            query = SearchQuery(words[0])
            for word in words[1:]:
                query = query | SearchQuery(word)

            items = Item.objects.annotate(rank=SearchRank(vector,
                query)).order_by('-rank')

            return render(request, 'lnf/search.html',
                    {'search_string': search_string, 'items': items})

    return HttpResponseRedirect('/')
