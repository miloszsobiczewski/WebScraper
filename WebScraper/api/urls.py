from django.urls import path
from . import views

urlpatterns = [
    path('', views.webscraper, name="api"),
    path('tasks/', views.status, name="tasks"),
    path('site/', views.site, name="site"),
]
