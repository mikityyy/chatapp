from django.urls import path, include
from . import views
from .views import PasswordChangeView
from django.contrib.auth import views as auth_views
from allauth.account.views import LoginView, LogoutView, SignupView


urlpatterns = [
    path('', views.index, name='index'),
    
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:pk>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    
    path('username_change', views.username_change, name='username_change'),
    path('email_change', views.email_change, name='email_change'),
    path('thumbnail_change', views.thumbnail_change, name='thumbnail_change'),
    path('password_change', views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/', include('allauth.urls')),
]
