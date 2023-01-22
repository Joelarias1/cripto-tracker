from django.urls import path
from . import views


urlpatterns = [
    path('welcome', views.welcome, name='welcome'),
    path('coin/<str:coin_id>/', views.coin_detail, name='coin_detail'),
    path('exchanges/', views.exchanges, name='exchanges')
]
