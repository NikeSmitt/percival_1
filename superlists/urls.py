from django.contrib import admin
from django.urls import path

from lists import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('lists/new', views.new_list, name='new_list'),
    path('lists/single-list-in-world/', views.view_list, name='view_list'),
]
