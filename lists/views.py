from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    """Show home page"""
    return HttpResponse('<html>'
                        '<title>To-Do lists</title>'
                        '</html>')
