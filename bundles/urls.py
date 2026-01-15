from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('payment/', views.payment, name='payment'),
    path('api/stk-push/', views.initiate_stk, name='initiate_stk'),
    path('api/mpesa/callback', views.mpesa_callback, name='mpesa_callback'),
]
