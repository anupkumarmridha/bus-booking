from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

# Create your models here.
from django.db import models
from home.models import Schedule, Stop, Seat
from accounts.models import User
from notification.models import Notification
from django.core.mail import send_mail
from busbooking import settings

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


@receiver(pre_delete, sender=Booking)
def set_seats_available(sender, instance, **kwargs):
    for seat in instance.seats.all():
        seat.is_available = True
        seat.save()


@receiver(post_save, sender=Booking)
def create_notification(sender, instance, created, **kwargs):
    if created and instance.status == "confirmed":
        # New booking was created with confirmed status
        message = f"Your booking ({instance.id}) has been confirmed."
        notification_type = "booking_confirmed"
        send_mail(
                f"Booking confirmation ({instance.id})",
                message,
                settings.EMAIL_FROM,  # Replace with your email address
                [instance.user.email],  # Replace with the user's email address
                fail_silently=False,
            )
    elif not created and instance.status == "confirmed":
        # Booking status was updated to confirmed
        message = f"Your booking ({instance.id}) has been confirmed."
        notification_type = "booking_confirmed"
        send_mail(
                f"Booking confirmation ({instance.id})",
                message,
                settings.EMAIL_FROM,  # Replace with your email address
                [instance.user.email],  # Replace with the user's email address
                fail_silently=False,
            )
    elif not created and instance.status == "pending":
        # Booking status was updated to pending
        message = f"Your payment is {instance.status}"
        notification_type = "booking_updated"
        
    elif not created and instance.status == "cancelled":
        # Booking status was updated to cancelled
        message = f"Your booking ({instance.id}) has been cancelled."
        notification_type = "booking_cancelled"
        send_mail(
                f"Booking cancelation ({instance.id})",
                message,
                settings.EMAIL_FROM,  # Replace with your email address
                [instance.user.email],  # Replace with the user's email address
                fail_silently=False,
            )
    else:
        # No new notification needed
        return
    
    # Create the notification object
    Notification.objects.create(
        user=instance.user,
        message=message,
        notification_type=notification_type
    )
        
    

@receiver(post_save, sender=Booking)
def update_schedule_total_available_seats_on_bus(sender, instance, **kwargs):
    schedule = instance.schedule
    total_available_seats_on_bus = schedule.bus.seat_set.filter(
        is_available=True
    ).count()
    schedule.total_available_seats_on_bus = total_available_seats_on_bus
    schedule.save()


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    )

    METHOD_CHOICES = (
        ("credit_card", "Credit Card"),
        ("debit_card", "Debit Card"),
        ("upi", "UPI"),
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
