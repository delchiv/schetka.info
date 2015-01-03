from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import resolve

from .models import Item

# Create your views here.
def home_page(request):
    if request.POST:
        Item.objects.create(text=request.POST.get('item_text', ''))
        return redirect('/lists/new-list/')

    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items':items,})
