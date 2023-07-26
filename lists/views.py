from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    """Show home page"""
    
    return render(request, 'lists/home.html')


def view_list(request):
    """Представление списка"""
    items = Item.objects.all()
    context = {
        'items': items,
    }
    
    return render(request, 'lists/list.html', context)


def new_list(request):
    """Создание нового списка"""
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/single-list-in-world/')
