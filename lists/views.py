from django.shortcuts import render
from django.shortcuts import HttpResponse


def home_page(request):
    """Домашняя страница"""
    return render(request, 'lists/home_page.html', {'new_item_text': request.POST.get('item_text', '')})


