from configparser import RawConfigParser
import redis

from ..constant import Service as Service_Key
from .base import Service


class RedisService(Service):

    def init(self, services):
        self.config_args_service = services.get_service(
            Service_Key.CONFIG_ARGS)
        self.redis_client = None

    def start(self):
        self.redis_client = redis.StrictRedis(
            **self.config_args_service.config_args
        )

    def close(self):
        self.redis_client.close()
        del self.redis_client
        del self.config_args_service

    def execute_command(self, command: str):
        return self.redis_client.execute_command(command)

    def execute_method(self, method: str, **kwargs):
        method_ins = getattr(self.redis_client, method)
        return method_ins(**kwargs)
