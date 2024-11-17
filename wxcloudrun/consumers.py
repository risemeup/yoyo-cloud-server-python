import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
logger = logging.getLogger('log')

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print(type(text_data), text_data)
        logger.info('receive: {}'.format(text_data))
        message = {
            'message': text_data
        }
        await self.send(text_data=json.dumps(message))
        logger.info('send: {}'.format(message))
