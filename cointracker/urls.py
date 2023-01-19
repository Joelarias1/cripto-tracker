from django.urls import path
from . import views


urlpatterns = [
    path('welcome', views.welcome, name='welcome'),
    path('coin/<str:coin_id>/', views.coin_detail, name='coin_detail'),
    path('coin-list', views.coinlist, name='coin-list')
]
