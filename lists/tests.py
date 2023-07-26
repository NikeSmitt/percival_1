from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

from lists.models import Item, List


class HomePageTest(TestCase):
    """Тест домашней страницы"""
    
    def test_home_page_returns_correct_html(self):
        """Test home page gives right response"""
        response: HttpResponse = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


class ListAndItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        
        list_ = List()
        list_.save()
        
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()
        
        second_item = Item()
        second_item.text = 'Second list item'
        second_item.list = list_
        second_item.save()
        
        save_list = List.objects.first()
        self.assertEqual(save_list, list_)
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        self.assertEqual(saved_items[0].text, 'The first (ever) list item')
        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].text, 'Second list item')
        self.assertEqual(saved_items[1].list, list_)


class ListViewTest(TestCase):
    
    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='Item_1', list=list_)
        Item.objects.create(text='Item_2', list=list_)
        
        response = self.client.get('/lists/single-list-in-world/')
        
        self.assertContains(response, 'Item_1')
        self.assertContains(response, 'Item_2')
    
    def test_uses_list_template(self):
        response = self.client.get('/lists/single-list-in-world/')
        self.assertTemplateUsed(response, 'lists/list.html')


class NewListTest(TestCase):
    """Тест нового списка"""
    
    def test_can_save_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
    
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/single-list-in-world/')
