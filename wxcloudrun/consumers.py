import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
import uuid
from datetime import datetime
from typing import List, Union
from enum import Enum
from dataclasses import dataclass, asdict
logger = logging.getLogger('log')

class Role(Enum):
    SERVER = "server"
    CLIENT = "client"

class MessType(Enum):
    TEXT = "text"
    OPTIONS = "options"

@dataclass
class TextContent:
    text: str

@dataclass
class Option:
    id: str
    label: str

@dataclass
class OptionContent:
    text : str
    options: List[Option]
    multiSelect: bool

@dataclass
class Message:
    role: str
    type: str
    id: str
    timestamp: str
    content: Union[TextContent, OptionContent]


def create_uuid() -> str:
    return str(uuid.uuid4())

def get_cur_time_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        mess = Message(
            role=Role.SERVER.value,
            type=MessType.TEXT.value,
            id=create_uuid(),
            timestamp=get_cur_time_str(),
            content=TextContent("你好哇！我是你的旅行助手yoyo！请告诉我你想去哪旅行？"),
        )
        await self.send_message(mess)
        logger.info('connect success!')

    async def disconnect(self, close_code):
        logger.info('disconnect!')

    # 直接返回接收到消息
    async def receive(self, text_data):
        logger.info('receive: {}'.format(text_data))
        try:
            mess = Message(**json.loads(text_data))
        except ValueError as e:
            logger.error(f"无法将接收到的数据转换为JSON格式: {e}")
            return
        mess.role = Role.SERVER.value
        await self.send_message(mess)

    async def send_message(self, message: Message):
        """
        发送消息函数，将Message对象转换为字符串以便发送
        :param message: 要发送的Message对象
        :return: 转换后的字符串
        """
        try:
            message_str = json.dumps(asdict(message))
            await self.send(text_data=message_str)
            logger.info('send: {}'.format(message_str))
        except Exception as e:
            logger.error(f"发生异常: {e}")
            
