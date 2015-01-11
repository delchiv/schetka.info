from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import resolve
from django.core.exceptions import ValidationError

from .models import Item, List
from .forms import ItemForm

# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form':ItemForm(),})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.POST:
        form = ItemForm(data=request.POST)
        if form.is_valid():
            item = Item.objects.create(text=request.POST.get('text', ''), list=list_)
            return redirect(list_)

    return render(request, 'list.html', {'list':list_, 'form':form,})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        item = Item.objects.create(text=request.POST.get('text', ''), list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form':form})

