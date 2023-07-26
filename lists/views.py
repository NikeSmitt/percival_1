from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    """Show home page"""
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text', '')
        Item.objects.create(text=new_item_text)
        return redirect('/lists/single-list-in-world/')
    
    return render(request, 'lists/home.html')


def view_list(request):
    """Представление списка"""
    items = Item.objects.all()
    context = {
        'items': items,
    }
    
    return render(request, 'lists/list.html', context)


