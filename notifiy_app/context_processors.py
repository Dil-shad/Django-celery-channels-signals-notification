from .models import BroadcastNotification

def notifications_context(request):
    all_notifications = BroadcastNotification.objects.all()
    return {'notifications': all_notifications}
