from datetime import datetime
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Schedule, Route, Stop


# Create your views here.
def homeView(request):
    routes = Route.objects.all()
    context = {
        "routes": routes,
    }
    return render(request, "home/index.html", context)


def AllRoutes(request):
    AllRoutes = Route.objects.all()
    context = {
        "AllRoutes": AllRoutes,
    }
    return render(request, "home/all_routes.html", context)


def allSchedules(request, pk):
    route = Route.objects.get(id=pk)
    AllSchedules = Schedule.objects.filter(route=route).order_by("departure_time")

    context = {
        "AllSchedules": AllSchedules,
        "route": route,
    }
    return render(request, "home/all_schedules.html", context)


def allStops(request, pk):
    route = Route.objects.get(id=pk)
    AllStops = Stop.objects.filter(route=route).order_by("departure_time")
    context = {
        "AllStops": AllStops,
        "route": route,
    }
    return render(request, "home/all_stops.html", context)
