from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

from lists.models import Item


class HomePageTest(TestCase):
    """Тест домашней страницы"""
    
    def test_home_page_returns_correct_html(self):
        """Test home page gives right response"""
        response: HttpResponse = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')
    
    def test_can_save_POST_request(self):
        data = {'item_text': 'New item text'}
        response: HttpResponse = self.client.post('/', data)
        
        self.assertEqual(Item.objects.count(), 1)
        first_item = Item.objects.first()
        self.assertEqual(first_item.text, 'New item text')
    
    def test_redirect_after_POST(self):
        data = {'item_text': 'New item text'}
        response: HttpResponse = self.client.post('/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/single-list-in-world/')
    
    def test_item_save_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
        
    def test_displays_all_list_items(self):
        Item.objects.create(text='Item_1')
        Item.objects.create(text='Item_2')
        
        response = self.client.get('/')
        
        self.assertIn('Item_1', response.content.decode())
        self.assertIn('Item_2', response.content.decode())
        
        


class ItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()
        
        second_item = Item()
        second_item.text = 'Second list item'
        second_item.save()
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        self.assertEqual(saved_items[0].text, 'The first (ever) list item')
        self.assertEqual(saved_items[1].text, 'Second list item')
