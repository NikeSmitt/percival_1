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
