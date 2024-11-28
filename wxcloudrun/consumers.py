import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
import uuid
from datetime import datetime
from typing import List, Union
from enum import Enum
logger = logging.getLogger('log')

class Role(Enum):
    SERVER = "server"
    CLIENT = "client"

class MessType(Enum):
    TEXT = "text"
    OPTIONS = "options"

class TextContent:
    def __init__(self, text: str):
        self.text = text

class Option:
    def __init__(self, id: str, label: str):
        self.id = id
        self.label = label

class OptionContent:
    def __init__(self, text, options: List[Option], multiSelect: bool):
        self.text = text
        self.options = options
        self.multiSelect = multiSelect

class Option:
    def __init__(self, id: str, label: str):
        self.id = id
        self.label = label

class Message:
    def __init__(self, role: str, type: str, id: str, timestamp: str, content: Union[TextContent, OptionContent]):
        self.role = role
        self.type = type
        self.id = id
        self.timestamp = timestamp
        self.content = content

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
        self.send_message(mess)
        logger.info('connect success!')

    async def disconnect(self, close_code):
        logger.info('disconnect!')

    # 直接返回接收到消息
    async def receive(self, text_data):
        logger.info('receive: {}, type:{}'.format(text_data, type(text_data)))
        logger.info('000')
        try:
            mess = self.json_to_message(text_data)
        except ValueError as e:
            logger.error(f"无法将接收到的数据转换为JSON格式: {e}")
            return
        logger.info('111')
        mess.role = Role.SERVER.value
        logger.info('222')
        try:
            logger.info('444')
            self.send_message(mess)
            message = {
            "type": "text",
            "id": "123",
            "timestamp": "2024-11-20 12:12:12",
            "content": {
                "text": "hello"
            }
            }
            await self.send(text_data=json.dumps(message))
            logger.info('555')
        except Exception as e:
            logger.info('666')
            logger.error(f"发生异常: {e}")
        logger.info('333')
        
    
    async def send_message(self, message: Message):
        """
        发送消息函数，将Message对象转换为字符串以便发送
        :param message: 要发送的Message对象
        :return: 转换后的字符串
        """
        try:
            logger.info('send_message: {}'.format(message))
            message_str = self.message_to_json(message)
            logger.info('befor send: {}'.format(message_str))
            await self.send(text_data=message_str)
            logger.info('send: {}'.format(message_str))
        except Exception as e:
            logger.error(f"发生异常: {e}")
    
    def json_to_message(self, received_data_str: str) -> Message:
        """
        Parses a JSON-encoded string into a Message object.

        This function takes a string representing JSON data and attempts to parse it
        into a Message object. If the input string is not a valid JSON, a ValueError
        is raised. The JSON data must contain the fields 'role', 'type', 'id',
        'timestamp', and 'content'. The 'content' field can either be a text or
        options. If the 'content' includes 'text', it is parsed as TextContent. If it
        includes 'options', it is parsed as OptionContent with a list of options and
        a multiSelect flag.

        :param received_data_str: The JSON string to be parsed.
        :return: A Message object constructed from the provided JSON data.
        :raises ValueError: If the provided string is not valid JSON or contains
                            invalid content data.
        """
        try:
            logger.info('received_data_str: {}'.format(received_data_str))
            received_data = json.loads(received_data_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"无法将接收到的数据转换为JSON格式: {e}")

        role = received_data.get('role')
        msg_type = received_data.get('type')
        id = received_data.get('id')
        timestamp = received_data.get('timestamp')
        content_data = received_data.get('content')

        if msg_type == MessType.TEXT.value:
            content = TextContent(content_data['text'])
        elif msg_type == MessType.OPTIONS.value:
            options = [Option(opt['id'], opt['label']) for opt in content_data['options']]
            multiSelect = content_data['multiSelect']
            content = OptionContent(options, multiSelect)
        else:
            raise ValueError("无效的接收数据内容")

        return Message(role, msg_type, id, timestamp, content)

    def message_to_json(self, message: Message) -> str:
        """
        Converts a Message object to a JSON string.

        This function takes a Message object and converts it to a JSON string.
        The JSON string contains the fields 'role', 'type', 'id', 'timestamp',
        and 'content'. The 'content' field depends on the type of the message.
        If the message type is 'text', the content field contains a text string.
        If the message type is 'options', the content field contains a list of
        options and a multiSelect flag.

        :param message: The Message object to be converted to a JSON string.
        :return: A JSON string representing the Message object.
        """
        message_dict = {
            'role': message.role,
            'type': message.type,
            'id': message.id,
            'timestamp': message.timestamp,
        }
        logger.info('aaa message_dict: {}'.format(message_dict))
        
        content_dict = {}
        if isinstance(message.content, TextContent):
            content_dict['text'] = message.content.text
        elif isinstance(message.content, OptionContent):
            options_list = []
            for option in message.content.options:
                options_list.append({
                    'id': option.id,
                    'label': option.label
                })
            content_dict['options'] = options_list
            content_dict['multiSelect'] = message.content.multiSelect

        logger.info('bbb message_dict: {}'.format(message_dict))
        message_dict['content'] = content_dict
        logger.info('ccc message_dict: {}'.format(message_dict))

        return json.dumps(message_dict)
