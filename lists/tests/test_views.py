from django.test import TestCase

from lists.models import Item, List


class HomePageTest(TestCase):
    """Тест домашней страницы"""
    
    def test_home_page_returns_correct_html(self):
        """Test home page gives right response"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')
    
    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Item_1', list=correct_list)
        Item.objects.create(text='Item_2', list=correct_list)
        
        other_list = List.objects.create()
        Item.objects.create(text='Other_Item_1', list=other_list)
        Item.objects.create(text='Other_Item_2', list=other_list)
        
        response = self.client.get(f'/lists/{correct_list.id}/')
        
        self.assertContains(response, 'Item_1')
        self.assertContains(response, 'Item_2')
        self.assertNotContains(response, 'Other_Item_1')
        self.assertNotContains(response, 'Other_Item_1')
    
    def test_passes_correct_list_to_template(self):
        """Тест: Проверяем, что передается правильный список в шаблон"""
        correct_list = List.objects.create()
        other_list = List.objects.create()
        
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
    """Тест нового списка"""
    
    def test_can_save_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
    
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
    """Тест нового элемента списка"""
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        """Тестируем сохранение элемента в существующий список"""
        
        correct_list = List.objects.create()
        other_list = List.objects.create()
        
        self.client.post(f'/lists/{correct_list.id}/add_item', data={
            'item_text': 'A new item for the correct list'
        })
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for the correct list')
        self.assertEqual(new_item.list, correct_list)
        self.assertNotEqual(new_item.list, other_list)
    
    def test_redirects_to_list_view(self):
        """Тестируем редирект после создания нового элемента списка"""
        
        correct_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.post(f'/lists/{correct_list.id}/add_item', data={
            'item_text': 'A new item for the correct list'
        })
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
