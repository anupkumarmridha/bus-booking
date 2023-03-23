from django.contrib import admin
from home.models import (
    Bus,
    BusRoute,
    BusSchedule,
    Seat,
    Booking,
    Payment,
    Notification,
    Cancellation,
)

# Register your models here.
admin.site.register(Bus)
admin.site.register(BusRoute)
admin.site.register(BusSchedule)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Notification)
admin.site.register(Cancellation)
