from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List


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

    def test_cannot_save_empty_list_items(self):
        """Тест: нельзя добавлять пустые элементы списка"""
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
        
    def test_invalid_list_items_arent_saved(self):
        """Тест: не допустимые элементы списка не сохраняются"""
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
        
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
        