from django.db import models
from accounts.models import User

# models.py

from django.db import models
from django.urls import reverse
from django.utils import timezone


class Bus(models.Model):
    bus_no = models.CharField(max_length=50)
    BUS_TYPES = [
        ("standard", "Standard"),
        ("deluxe", "Deluxe"),
        ("vip", "VIP"),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=BUS_TYPES)
    amenities = models.TextField(blank=True)
    capacity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.bus_no}"


class Route(models.Model):
    departure_location = models.CharField(max_length=100)
    arrival_location = models.CharField(max_length=100)
    distance = models.IntegerField()
    travel_time = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.departure_location} - {self.arrival_location}"


class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bus.name} - {self.route.departure_location} to {self.route.arrival_location}"


class Seat(models.Model):
    SEAT_CATEGORIES = [
        ("standard", "Standard"),
        ("deluxe", "Deluxe"),
        ("vip", "VIP"),
    ]
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    category = models.CharField(max_length=20, choices=SEAT_CATEGORIES)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bus.name} - {self.seat_number} ({self.category})"
