import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Appointment

logger = logging.getLogger(__name__)

class AppointmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("WebSocket connect attempt")
        try:
            # Join the appointments group
            await self.channel_layer.group_add("appointments", self.channel_name)
            await self.accept()
            
            # Send initial data
            initial_data = await self.get_initial_data()
            await self.send(text_data=json.dumps({
                'type': 'initial_data',
                'data': initial_data
            }))
            logger.info("WebSocket connected and initial data sent")
        except Exception as e:
            logger.error(f"Error in connect: {str(e)}")
            raise

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("appointments", self.channel_name)
        logger.info(f"WebSocket disconnected with code: {close_code}")

    async def appointment_update(self, event):
        """
        Handle appointment updates and send to WebSocket
        """
        try:
            await self.send(text_data=json.dumps({
                'type': 'appointment_update',
                'data': event['data']
            }))
            logger.info("Update sent to client")
        except Exception as e:
            logger.error(f"Error sending update: {str(e)}")

    @database_sync_to_async
    def get_initial_data(self):
        """
        Get all appointments for initial data load
        """
        return list(Appointment.objects.values('id', 'name', 'status')) 