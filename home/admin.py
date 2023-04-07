from django.contrib import admin
from home.models import (
    Bus,
    Route,
    Stop,
    Schedule,
    Seat,
)

# Register your models here.
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(Schedule)
admin.site.register(Seat)
