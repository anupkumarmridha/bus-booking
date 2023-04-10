from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

# Create your models here.
from django.db import models
from home.models import Schedule, Stop, Seat
from accounts.models import User
from notification.models import Notification


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_location = models.ForeignKey(
        Stop, on_delete=models.CASCADE, related_name="source_bookings"
    )
    destination_location = models.ForeignKey(
        Stop, on_delete=models.CASCADE, related_name="destination_bookings"
    )
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    total_seats = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default="pending")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    travel_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.schedule.route.departure_location} to {self.schedule.route.arrival_location}"

    def count_seats(self):
        return self.seats.count()

    def calculate_amount(self):
        distance = self.destination_location.km - self.source_location.km
        amount = distance * 10 * self.total_seats
        return amount


@receiver(pre_delete, sender=Booking)
def set_seats_available(sender, instance, **kwargs):
    for seat in instance.seats.all():
        seat.is_available = True
        seat.save()


@receiver(post_save, sender=Booking)
def create_notification(sender, instance, created, **kwargs):
    if not created and instance.status == "pending":
        # Booking was updated with new status
        message = f"Your payment is {instance.status}"
        notification_type = "booking_updated"
    elif created and instance.status == "confirmed":
        # New booking was created with confirmed status
        message = f"Your booking ({instance.id}) has been confirmed."
        notification_type = "booking_confirmed"
    else:
        # No new notification needed
        return

    # Create new Notification object for the user
    notification = Notification.objects.create(
        user=instance.user, message=message, notification_type=notification_type
    )


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
