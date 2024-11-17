import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
logger = logging.getLogger('django')

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        logger.info('receive: ',str(text_data))
        await self.send(text_data=json.dumps({
            'message': text_data
        }))
        logger.info('send: ', str(text_data))
