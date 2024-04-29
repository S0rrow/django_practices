from django.urls import path
from mypolls import views

app_name = 'polls'

urlpatterns = [
    path('', views.index),
    path('<int:question_id>/', views.detail),
    path('<int:question_id>/vote', views.vote, name="vote"),
    path('<int:question_id>/results', views.results, name='results')
]
