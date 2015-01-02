from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Item

# Create your views here.
def home_page(request):
    if request.POST:
        Item.objects.create(text=request.POST.get('item_text', ''))
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items':items,})
