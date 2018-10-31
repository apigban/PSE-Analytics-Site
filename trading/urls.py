from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='trading-home'),
    #path('home/', views.home, name='trading-home'),
    path('about/', views.about, name='trading-about'),
    path('search/', views.search, name='trading-search'),
]