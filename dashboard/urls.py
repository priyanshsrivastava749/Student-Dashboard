from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('submit-homework/', views.submit_homework, name='submit_homework'),
    path('ask-doubt/', views.ask_doubt, name='ask_doubt'),
    path('create-assignment/', views.create_assignment, name='create_assignment'),
    path('upload-checked-copy/<int:homework_id>/', views.upload_checked_copy, name='upload_checked_copy'),
]
# Touch
