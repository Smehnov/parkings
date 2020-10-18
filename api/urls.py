from django.urls import path

from . import views

urlpatterns = [
    path('email', views.email, name='email'),
    path('parkings', views.get_parkings, name='parkings')
]
