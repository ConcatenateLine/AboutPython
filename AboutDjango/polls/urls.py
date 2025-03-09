from django.urls import path
from .views import authviews, views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='home'),
    path('login/', authviews.login, name='login'),
    path('logout/', authviews.logout, name='logout'),
    path('register/', authviews.register, name='register'),
    
    path('polls/', views.IndexView.as_view(), name='dashboard'),
    path('polls/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('polls/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
    path('polls/indexupload/', views.IndexUploadView, name='indexupload'),
    path('polls/success/', views.success, name='success'),
    path('polls/upload/', views.upload, name='upload'),
    path('polls/listupload/', views.ListUploadView.as_view(), name='listupload'),
]
