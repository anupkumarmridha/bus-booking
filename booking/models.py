from django.db import models

# Create your models here.
from django.db import models
from home.models import Schedule
from accounts.models import User


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seats = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.schedule.route.departure_location} to {self.schedule.route.arrival_location}"


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    )

    METHOD_CHOICES = (
        ("credit_card", "Credit Card"),
        ("debit_card", "Debit Card"),
        ("net_banking", "Net Banking"),
        ("upi", "UPI"),
        ("wallet", "Wallet"),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking.user.username} - {self.booking.schedule.route.departure_location} to {self.booking.schedule.route.arrival_location} - {self.amount}"


# class Cancellation(models.Model):
#     booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.booking.user.username} - {self.booking.bus_schedule.bus.bus_no} ({self.timestamp.date()})"
