from django.urls import path
from booking import views

# app_name = 'home'
urlpatterns = [
    path("/booking/<int:route_id>/<int:schedule_id>", views.booking, name="booking"),
    path("/booking/<int:booking_id>", views.makePayment, name="makePayment"),
    path(
        "/booking-confirm/<int:booking_id>",
        views.bookingConfirmation,
        name="bookingConfirmation",
    ),
    path(
        "/all-bookings",
        views.allBookings,
        name="allBookings",
    ),
]
