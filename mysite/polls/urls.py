from django.urls import path

from . import views
from .views import register, logout_user, login_user, edit_profile, profile, delete_profile, detail_view, CreatePollView

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:question_id>/', detail_view, name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('delete-profile/', delete_profile, name='delete-profile'),
    path('profile/', profile, name='profile'),
    path('create/', CreatePollView.as_view(), name='create_poll'),
]