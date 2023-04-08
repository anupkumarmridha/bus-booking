from django.urls import path
from booking import views

# app_name = 'home'
urlpatterns = [
    path("/booking/<int:id>", views.booking, name="booking"),
]
