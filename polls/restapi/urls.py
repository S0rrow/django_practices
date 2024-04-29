from django.urls import path
from restapi import views

app_name='api'

urlpatterns = [
    path('knn/', views.knn),
]