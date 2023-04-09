from django.shortcuts import render, redirect
from home.models import Route, Stop, Seat, Schedule, Bus
from booking.models import Booking
from django.contrib import messages


# Create your views here.
def booking(request, route_id, schedule_id):
    route = Route.objects.get(pk=route_id)
    AllStops = Stop.objects.filter(route=route).order_by("departure_time")
    schedule = Schedule.objects.get(pk=schedule_id)
    allSeats = Seat.objects.filter(bus=schedule.bus, is_available=True).order_by(
        "seat_number"
    )
    if request.method == "POST":
        user = request.user
        source_stop_id = request.POST.get("source_location")
        destination_stop_id = request.POST.get("destination_location")
        travel_date = request.POST.get("travel_date")

        source_location = Stop.objects.get(id=source_stop_id)
        destination_location = Stop.objects.get(id=destination_stop_id)

        seat_ids = request.POST.getlist("seat_ids")
        print(seat_ids)
        seats = Seat.objects.filter(id__in=seat_ids)
        distance = source_location.km - destination_location.km
        print(distance)
        booking = Booking.objects.create(
            user=user,
            source_location=source_location,
            destination_location=destination_location,
            schedule=schedule,
            travel_date=travel_date,
            total_seats=seats.count(),
        )
        booking.seats.set(seats)
        saved_booking = booking.save()
        if saved_booking:
            messages.success(request, "Success  😎")

    context = {
        "route": route,
        "AllStops": AllStops,
        "allSeats": allSeats,
        "schedule": schedule,
    }
    return render(request, "booking/booking.html", context)
