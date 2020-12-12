import functools
import time
import pika
import json
import uuid
import re



from utils.config import global_config
from utils.logger import LOGGER
from datas.Response import Response
from impl.ClientConsumer import AsyncConsumer

class AMQPClient_Consumer(AsyncConsumer):
    def __init__(self, amqp_url, exchange, exchange_type, queue, prefetch_count, durable=True):
        # Init Super Class
        super().__init__(amqp_url, exchange, exchange_type,queue, prefetch_count, durable=True)
    
    def on_message(self, _unused_channel, basic_deliver, properties, body):
        try:
            LOGGER.info(f"{properties}")
            LOGGER.info(f"{body}")
        except Exception as e:
            LOGGER.error(f"AMQPClient_Consumer : {e}")
        finally:
            self.acknowledge_message(basic_deliver.delivery_tag)

class AMQP_Client(object):
    def __init__(self, amqp_url, prefetch_count):
        self._reconnect_delay = 0
        self._amqp_url = amqp_url
        self.queue = "%s" % global_config._get(
            "queue", "client_apm_processing_queue", "ha_ops_apm_processing")
        self.exchange = 'message'
        self.exchange_type = 'topic'
        self.prefetch_count = prefetch_count
        self._consumer = AMQPClient_Consumer(
            self._amqp_url, exchange=self.exchange, exchange_type=self.exchange_type, queue=self.queue, prefetch_count=self.prefetch_count, durable=True)
    def run(self):
        while True:
            try:
                self._consumer.run()
            except KeyboardInterrupt:
                self._consumer.stop()
                break
            self._maybe_reconnect()

    def _maybe_reconnect(self):
        if self._consumer.was_consuming :
            self._consumer.stop()
            reconnect_delay = self._get_reconnect_delay()
            LOGGER.info('Reconnecting after %d seconds', reconnect_delay)
            time.sleep(reconnect_delay)
            self._consumer = AMQPClient_Consumer(
                self._amqp_url, exchange=self.exchange, exchange_type=self.exchange_type, queue=self.queue, prefetch_count=self.prefetch_count, durable=True)

    def _get_reconnect_delay(self):
        if self._consumer.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay