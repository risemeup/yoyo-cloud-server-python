import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
import uuid
from datetime import datetime
logger = logging.getLogger('log')

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info('connect success!')

    async def disconnect(self, close_code):
        logger.info('disconnect!')

    async def receive(self, text_data):
        logger.info('receive: {}'.format(text_data))
        # 生成一个随机的UUID（通用唯一识别码），版本为4
        unique_id = uuid.uuid4()

        # 将UUID转换为字符串形式
        unique_string_id = str(unique_id)

        formatted_time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = {
            "type": "text",
            "id": unique_string_id,
            "timestamp": formatted_time_string,
            "content": {
                "text": text_data
            }
        }
        await self.send(text_data=json.dumps(message))
        logger.info('send: {}'.format(message))
