import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
logger = logging.getLogger('log')

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info('connect success!')

    async def disconnect(self, close_code):
        logger.info('disconnect!')

    async def receive(self, text_data):
        logger.info('receive: {}'.format(text_data))
        message = {
            "type": "text",
            "id": "1111",
            "timestamp": "2024-11-24 11:00:00",
            "content": {
                "text": '123'
                }
        }
        await self.send(text_data=json.dumps(message))
        logger.info('send: {}'.format(message))