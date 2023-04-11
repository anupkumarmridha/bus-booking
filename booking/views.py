from django.shortcuts import render, redirect, reverse, HttpResponse
from home.models import Route, Stop, Seat, Schedule, Bus
from booking.models import Booking, Payment
from django.contrib import messages
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth import get_user


# Create your views here.
def booking(request, route_id, schedule_id):
    middleware = AuthenticationMiddleware(get_user)
    middleware.process_request(request)
    if not request.user.is_authenticated:
        return HttpResponse("Submission outside this window is not allowed 😎")
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
        return redirect(makePayment, booking.pk)
    context = {
        "route": route,
        "AllStops": AllStops,
        "allSeats": allSeats,
        "schedule": schedule,
    }
    return render(request, "booking/booking.html", context)


def makePayment(request, booking_id):
    book = Booking.objects.get(id=booking_id)
    if request.method == "POST":
        method = request.POST.get("method")
        upi_id = request.POST.get("upi_id")
        card_holder_name = request.POST.get("card_holder_name")
        card_number = request.POST.get("card_number")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")
        status = "paid"
        if upi_id or (card_holder_name and card_number and expiry_date and cvv):
            payment = Payment.objects.create(
                booking_id=booking_id, method=method, amount=book.amount, status=status
            )
            payment.save()
            book.status = "confirmed"
            book.save()
            messages.success(request, "confirmed  😎")
            return redirect(bookingConfirmation, book.pk)
    method_choices = Payment.METHOD_CHOICES
    context = {
        "book": book,
        "method_choices": method_choices,
    }
    return render(request, "booking/payment.html", context)


def bookingConfirmation(request, booking_id):
    book = Booking.objects.get(id=booking_id)
    context = {
        "book": book,
    }
    return render(request, "booking/confirm.html", context)
