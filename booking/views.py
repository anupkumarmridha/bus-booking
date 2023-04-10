from django.shortcuts import render, redirect, reverse
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
        print(source_stop_id)
        if "Source Location" in source_stop_id:
            messages.error(request, "Please select source Location!")
            return redirect(reverse("booking", args=(route_id, schedule_id)))
        if "Destination Location" in destination_stop_id:
            messages.error(request, "Please select Destination Location!")
            return redirect(reverse("booking", args=(route_id, schedule_id)))

        total_price = request.POST.get("total_price")
        travel_date = request.POST.get("travel_date")

        source_location = Stop.objects.get(id=source_stop_id)
        destination_location = Stop.objects.get(id=destination_stop_id)

        seat_ids = request.POST.getlist("seat_ids")
        seats = Seat.objects.filter(id__in=seat_ids)
        print(seats)

        booking = Booking.objects.create(
            user=user,
            source_location=source_location,
            destination_location=destination_location,
            schedule=schedule,
            total_seats=seats.count(),
            amount=total_price,
            travel_date=travel_date,
        )
        booking.seats.set(seats)
        for seat in seats:
            seat.is_available = False
            seat.save()
        booking.save()

        messages.success(request, "Success  😎")

    context = {
        "route": route,
        "AllStops": AllStops,
        "allSeats": allSeats,
        "schedule": schedule,
    }
    return render(request, "booking/booking.html", context)
