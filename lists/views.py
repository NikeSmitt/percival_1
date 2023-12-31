from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Item, List


def home_page(request):
    """Show home page"""
    
    return render(request, 'lists/home.html')


def view_list(request, pk: int):
    """Представление списка"""
    list_ = List.objects.get(id=pk)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = 'You can\'t have an empty list item'

    return render(request, 'lists/list.html', {'list': list_, 'error': error})


def new_list(request):
    """Создание нового списка"""
    
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = 'You can\'t have an empty list item'
        return render(request, 'lists/home.html', {'error': error})
    return redirect(list_)
