from django.urls import path
from . import views

app_name = 'calendar'
urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path(r'new/', views.calendar_new, name='calendar_new'),

    path(r'objective/new/', views.event, name='objective_new'),
    path(r'objective/show/<str:objective_id>/', views.show_objective, name='objective_show'),
    path(r'objective/edit/<str:objective_id>/', views.event, name='objective_edit'),
    path(r'objective/delete/<str:objective_id>/', views.delete_objetive, name='objective_delete'),
    path(r'change_format/', views.change_format, name='change_format'),
    path(r'others_calendars/', views.others_calendars, name='others_calendars'),

    path(r'shared/<str:calendar_slug>/', views.show_calendar.as_view(), name='show_calendar'),
    path(r'shared/<str:calendar_slug>/new/', views.shared_calendar_new, name='shared_calendar_new'),
    path(r'shared/<str:calendar_slug>/objective/new/', views.shared_event, name='shared_objective_new'),
    path(r'shared/<str:calendar_slug>/objective/show/<str:objective_id>/', views.shared_show_objective, name='shared_objective_show'),
    path(r'shared/<str:calendar_slug>/objective/edit/<str:objective_id>/', views.shared_event, name='shared_objective_edit'),
    path(r'shared/<str:calendar_slug>/objective/delete/<str:objective_id>/', views.shared_delete_objetive, name='shared_objective_delete'),
    path(r'shared/<str:calendar_slug>/change_format/', views.shared_change_format, name='shared_change_format'),
    path(r'shared/<str:calendar_slug>/others_calendars/', views.shared_others_calendars, name='shared_others_calendars'),
]
