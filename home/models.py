from django.db import models
from accounts.models import User


class Bus(models.Model):
    bus_no = models.CharField(max_length=50)
    bus_type = models.CharField(max_length=50)
    capacity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus_no


class BusRoute(models.Model):
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.origin} - {self.destination}"


class BusSchedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bus.bus_no} - {self.bus_route.origin} to {self.bus_route.destination}"


class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_no = models.CharField(max_length=5)
    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.seat_no} ({self.bus.bus_no})"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus_schedule = models.ForeignKey(BusSchedule, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.bus_schedule.bus.bus_no} ({self.timestamp.date()})"


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.booking.user.username} - {self.booking.bus_schedule.bus.bus_no} ({self.amount})"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.timestamp.date()})"


class Cancellation(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking.user.username} - {self.booking.bus_schedule.bus.bus_no} ({self.timestamp.date()})"
