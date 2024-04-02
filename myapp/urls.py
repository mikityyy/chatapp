from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:pk>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('logout', views.logout_view, name='logout_view'),
    path('username_change', views.username_change, name='username_change'),
    path('email_change', views.email_change, name='email_change'),
]
