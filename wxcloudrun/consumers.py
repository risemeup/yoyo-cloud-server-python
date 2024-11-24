import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
import uuid
from datetime import datetime
from typing import List, Optional
from enum import Enum
logger = logging.getLogger('log')

class Role(Enum):
    SERVER = "server"
    CLIENT = "client"

class MessType(Enum):
    TEXT = "text"
    OPTIONS = "options"

class Option:
    def __init__(self, id: str, label: str):
        self.id = id
        self.label = label

class Message:
    def __init__(self, role: str, type: str, id: str, timestamp: str, text: str, options: Optional[List[Option]] = None,
                 multiSelect: Optional[bool] = None):
        self.role = role
        self.type = type
        self.id = id
        self.timestamp = timestamp
        self.text = text
        self.options = options
        self.multiSelect = multiSelect

def create_uuid() -> str:
    return str(uuid.uuid4())

def get_cur_time_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        mess = Message(
            role=Role.SERVER,
            type=MessType.TEXT,
            id=create_uuid(),
            timestamp=get_cur_time_str(),
            text="你好哇！我是你的旅行助手yoyo！请告诉我你想去哪旅行？"
        )
        self.send_message(mess)
        logger.info('connect success!')

    async def disconnect(self, close_code):
        logger.info('disconnect!')

    # 直接返回接收到消息
    async def receive(self, text_data):
        logger.info('receive: {}'.format(text_data))
        mess = self.receive_message(text_data)
        mess.role = Role.SERVER
        self.send_message(mess)
        
    
    async def send_message(self, message: Message):
        """
        发送消息函数，将Message对象转换为字符串以便发送
        :param message: 要发送的Message对象
        :return: 转换后的字符串
        """
        try:
            message1 = {
            "type": "text",
            "id": create_uuid(),
            "timestamp": get_cur_time_str(),
            "content": {
                "text": '123'
                }
            }
            await self.send(text_data=json.dumps(message1))
            # message_dict = {
            #     'role': message.role,
            #     'type': message.type,
            #     'id': message.id,
            #     'timestamp': message.timestamp,
            #     'text': message.text
            # }
            # if message.options:
            #     message_dict['options'] = [{'id': opt.id, 'label': opt.label} for opt in message.options]
            # if message.multiSelect:
            #     message_dict['multiSelect'] = message.multiSelect
            
            # await self.send(text_data=json.dumps(message_dict))
            logger.info('send: {}'.format(message1))
        except Exception as e:
            logger.error(f"发生异常: {e}")
    
    def receive_message(self, raw_data: str) -> Message:
        """
        接收消息函数，从原始数据字符串中解析出Message对象
        :param raw_data: 原始数据字符串，假设其格式符合Message类的结构要求
        :return: 解析出的Message对象
        """
        data_dict = eval(raw_data)  # 这里假设原始数据可以通过eval转换为字典，实际应用中可能需要更安全的解析方式

        role = data_dict.get('role')
        msg_type = data_dict.get('type')
        id = data_dict.get('id')
        timestamp = data_dict.get('timestamp')
        text = data_dict.get('text')
        options_data = data_dict.get('options')
        multiSelect = data_dict.get('multiSelect')

        options = None
        if options_data:
            options = [Option(opt['id'], opt['label']) for opt in options_data]

        return Message(role, msg_type, id, timestamp, text, options, multiSelect)

