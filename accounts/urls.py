from django.urls import path
from accounts import views

# app_name = 'home'
urlpatterns = [
    path("/signup/", views.handelSingup, name="handelSingup"),
    path("/login", views.handleLogin, name="handleLogin"),
    path("/logout", views.handleLogout, name="handleLogout"),
]
