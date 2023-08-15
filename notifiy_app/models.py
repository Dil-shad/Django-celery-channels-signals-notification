from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import json
from django.utils import timezone
# Create your models here.

class BroadcastNotification(models.Model):
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)

    
    class Meta:
        ordering = ['-broadcast_on']
        
'''
# Django signals allow you to react to events in your app.
# Create a signal handler function and connect it to an event.
'''       


# Example: When BroadcastNotification is saved, this function is called.
@receiver(post_save, sender=BroadcastNotification)
def notification_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notifications or you can create a dynamic task in Celery Beat
    if created:
        schedule, created  = CrontabSchedule.objects.get_or_create(
            hour=instance.broadcast_on.hour,
            minute=instance.broadcast_on.minute,
            day_of_month=instance.broadcast_on.day,
            month_of_year=instance.broadcast_on.month,
            timezone="Asia/Kolkata"   # Correct time zone spelling
        )
        task = PeriodicTask.objects.create(
            crontab=schedule,
            name="broadcast-notification-" + str(instance.id),
            task="notifiy_app.tasks.broadcast_notification",
            args=json.dumps((instance.id,))
        )
        # Schedule a task to delete the notification after 24 hours
        delete_schedule, _ = CrontabSchedule.objects.get_or_create(
            hour=(instance.broadcast_on).hour, #timezone.timedelta(hours=24)).hour,
            minute=(instance.broadcast_on + timezone.timedelta(minutes=2)).minute,
            day_of_month=(instance.broadcast_on + timezone.timedelta(minutes=2)).day,
            month_of_year=(instance.broadcast_on + timezone.timedelta(minutes=2)).month,
            timezone="Asia/Kolkata"
        )
        delete_task = PeriodicTask.objects.create(
            crontab=delete_schedule,
            name="delete-notification-" + str(instance.id),
            task="notifiy_app.tasks.delete_expired_notifications",
            args=json.dumps((instance.id,))
        )
        