from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# Create your views here.

app_name = 'chart'

urlpatterns = [
    path('', views.chart)
]