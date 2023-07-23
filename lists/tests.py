from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page


class HomePageTest(TestCase):
    """Тест домашней страницы"""
    
    def test_home_page_returns_correct_html(self):
        """Test home page gives right response"""
        response: HttpResponse = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_POST_request(self):
        """ """
        data = {'item_text': 'New item text'}
        response: HttpResponse = self.client.post('/', data)
        self.assertIn('New item text', response.content.decode())
        self.assertTemplateUsed(response, 'lists/home.html')
