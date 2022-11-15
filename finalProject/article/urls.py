from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('inputCrawling/', views.InputUrlCrawling),
    path('viewtest/', views.viewtest), 
    path('newsview/', views.main),
    path('newsview/result',views.result, name='result')
]