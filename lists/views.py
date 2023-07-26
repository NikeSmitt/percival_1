from django.shortcuts import render, redirect

from lists.models import Item, List


def home_page(request):
    """Show home page"""
    
    return render(request, 'lists/home.html')


def view_list(request, pk: int):
    """Представление списка"""
    list_ = List.objects.get(id=pk)
    context = {
        'list': list_
    }
    
    return render(request, 'lists/list.html', context)


def new_list(request):
    """Создание нового списка"""
    
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id: int):
    """Добавляем элемент"""
    list_ = List.objects.get(id=list_id)
    item_text = request.POST['item_text']
    Item.objects.create(text=item_text, list=list_)
    return redirect(f'/lists/{list_id}/')
