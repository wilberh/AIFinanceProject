from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views


urlpatterns = [
    path('trend/', views.GoogleTrendApiDetail.as_view(), name='trend')
]
