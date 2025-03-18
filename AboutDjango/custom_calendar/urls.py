from django.urls import path
from . import views

app_name = 'calendar'
urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path(r'objective/new/', views.event, name='objective_new'),
    path(r'objective/show/<str:objective_id>/', views.show_objective, name='objective_show'),
    path(r'objective/edit/<str:objective_id>/', views.event, name='objective_edit'),
    path(r'objective/delete/<str:objective_id>/', views.delete_objetive, name='objective_delete'),
    path(r'change_format/', views.change_format, name='change_format'),
]
