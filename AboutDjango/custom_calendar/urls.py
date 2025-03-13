from django.urls import path
from . import views

app_name = 'calendar'
urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path(r'objective/new/', views.event, name='objective_new'),
    path(r'objective/edit/<str:objective_id>/', views.event, name='objective_edit'),
]
