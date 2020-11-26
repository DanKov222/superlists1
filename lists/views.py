from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse

from .models import Item


def home_page(request):
    """Домашняя страница"""
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/single_list/')

    items = Item.objects.all()
    return render(request, 'lists/home_page.html', {'items': items})


def view_list(request):
    """представление списка"""
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})

