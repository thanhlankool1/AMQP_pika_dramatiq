from threading import Thread
import logging
import sys

from amqp.AMQPClient import AMQP_Client
from utils.config import global_config
from utils.logger import LOGGER


# Rabbit Cluster
url = "amqp://%s:%s@%s:%s/" % (global_config._get(
    "amqp", "amqp_user", "admin"), global_config._get(
    "amqp", "amqp_pass", "admin"), global_config._get(
    "amqp", "amqp_host", "localhost"), global_config._get(
    "amqp", "amqp_port", "5672"))


def amqp_client_worker():
    try:
        # Init Config
        amqp_client = AMQP_Client(url, prefetch_count=16)
        amqp_client.run()
    except Exception as e:
        LOGGER.error("%s" % e)

if __name__ == "__main__":
    try:
        amqp_client_worker_thread = Thread(target=amqp_client_worker)
        amqp_client_worker_thread.start()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        LOGGER.error("%s" % e)