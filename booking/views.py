from django.shortcuts import render
from home.models import Route, Stop


# Create your views here.
def booking(request, id):
    route = Route.objects.get(pk=id)
    AllStops = Stop.objects.filter(route=route).order_by("departure_time")
    if request.method == "POST":
        pass
    context = {
        "route": route,
        "AllStops": AllStops,
    }
    return render(request, "booking/booking.html", context)
