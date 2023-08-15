from django.shortcuts import render, HttpResponse
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync

# Create your views here.


def index(request):
    return render(request, 'index.html',{'room_name': "broadcast"})


#without celery ,trough channels
def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        
        {
            'type': 'send_notification',
            'message': json.dumps("Diwali sale")
        }
    )
    return HttpResponse("Done")