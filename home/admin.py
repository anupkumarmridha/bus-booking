from django.contrib import admin
from home.models import (
    Bus,
    Route,
    Schedule,
    Seat,
)

# Register your models here.
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Schedule)
admin.site.register(Seat)
