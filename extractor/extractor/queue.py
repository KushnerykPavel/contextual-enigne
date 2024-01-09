import json

import nats
from nats.aio.msg import Msg
from .content_processor import ContentProcessor


class Queue:
    def __init__(self, conn: nats.NATS, subject: str, content_processor: ContentProcessor):
        self._conn = conn
        self._subject = subject
        self._content_processor = content_processor

    async def subscribe_handler(self, msg: Msg):
        data = msg.data.decode()

        extractor_message = json.loads(data)
        processing_result = await self._content_processor.process_content(str(extractor_message['content']))

        extractor_message['detected_language'] = processing_result['detected_language']
        extractor_message['keywords'] = processing_result['keywords']
        extractor_message['categories'] = processing_result['categories']

        json_data = json.dumps(extractor_message)
        await self._conn.publish('contextual-engine-extractor-response', json_data.encode())

    async def subscribe(self):
        await self._conn.subscribe(self._subject, cb=self.subscribe_handler)
