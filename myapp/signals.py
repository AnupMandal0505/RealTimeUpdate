from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Appointment
import logging

logger = logging.getLogger(__name__)

@receiver([post_save, post_delete], sender=Appointment)
def appointment_update_handler(sender, instance=None, created=False, **kwargs):
    """
    Signal handler to send WebSocket updates when appointments change
    """
    try:
        # Get all appointments
        appointments = list(Appointment.objects.values('id', 'name', 'status'))
        
        # Get channel layer
        channel_layer = get_channel_layer()
        
        # Send update to all clients
        async_to_sync(channel_layer.group_send)(
            "appointments",
            {
                "type": "appointment_update",
                "data": appointments
            }
        )
        
        action = "created" if created else "updated"
        logger.info(f"Appointment {action}: {instance.name}")
    except Exception as e:
        logger.error(f"Error in appointment_update_handler: {str(e)}") 