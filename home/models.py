from django.db import models
from accounts.models import User
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.bus_no}"


class Seat(models.Model):
    SEAT_CATEGORIES = [
        ("window_seat", "window_seat"),
        ("aisle_seat", "aisle_seat"),
    ]
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="seat_set")
    seat_number = models.CharField(max_length=10)
    category = models.CharField(max_length=20, choices=SEAT_CATEGORIES)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["bus", "seat_number"]

    def __str__(self):
        return f"{self.seat_number} - {self.bus.name} - ({self.category})"


@receiver(post_save, sender=Bus)
def create_seats(sender, instance, created, **kwargs):
    if created or instance.capacity != instance.seat_set.count():
        Seat.objects.filter(bus=instance).delete()
        for i in range(instance.capacity):
            Seat.objects.create(
                bus=instance,
                seat_number=str(i + 1),
                category="aisle_seat" if i % 2 == 0 else "window_seat",
            )


class Route(models.Model):
    departure_location = models.CharField(max_length=100)
    arrival_location = models.CharField(max_length=100)
    distance = models.IntegerField()
    travel_time = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.departure_location} - {self.arrival_location}"


class Stop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="stops")
    location = models.CharField(max_length=100)
    km = models.FloatField()
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    duration = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["arrival_time"]

    def __str__(self):
        return f"{self.location} - {self.route}"

    def clean(self):
        if (
            self.arrival_time
            and self.departure_time
            and self.arrival_time >= self.departure_time
        ):
            raise ValidationError("Arrival time must be less than departure time.")

    def get_duration(self):
        """
        Returns the duration between the arrival time and the departure time
        as a timedelta object.
        """
        if self.arrival_time and self.departure_time:
            arrival = datetime.combine(datetime.today(), self.arrival_time)
            departure = datetime.combine(datetime.today(), self.departure_time)
            duration = departure - arrival
            return duration

    def save(self, *args, **kwargs):
        """
        Overrides the save method to calculate and set the duration field
        based on the arrival and departure times.
        """
        self.duration = self.get_duration()
        super().save(*args, **kwargs)


class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    duration = models.DurationField(null=True, blank=True)
    total_seats_on_bus = models.IntegerField(null=True, blank=True)
    total_available_seats_on_bus = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["departure_time"]

    def __str__(self):
        return f"{self.bus.name} - {self.route.departure_location} to {self.route.arrival_location} - {self.departure_time} - {self.arrival_time}"

    def clean(self):
        if (
            self.arrival_time
            and self.departure_time
            and self.departure_time >= self.arrival_time
        ):
            raise ValidationError("Departure time must be less than Arival time.")

    def get_duration(self):
        """
        Returns the duration between the arrival time and the departure time
        as a timedelta object.
        """
        if self.arrival_time and self.departure_time:
            arrival = datetime.combine(datetime.today(), self.arrival_time)
            departure = datetime.combine(datetime.today(), self.departure_time)
            duration = arrival - departure
            return duration

    def save(self, *args, **kwargs):
        """
        Overrides the save method to calculate and set the duration field
        based on the arrival and departure times.
        """
        self.total_seats_on_bus = self.bus.capacity
        self.total_available_seats_on_bus = self.bus.seat_set.filter(
            is_available=True
        ).count()
        self.duration = self.get_duration()
        super().save(*args, **kwargs)
