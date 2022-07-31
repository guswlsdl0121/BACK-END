from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.Login_view, name='Login'),
    path('login/callback', views.UserInfo_view, name='UserInfo'),
    path('logout/',views.Logout_view, name='Logout'),
]
