from configparser import RawConfigParser

from ..constant import Service as Service_Key
from .base import Service


class ConfigServiceLocal(Service):

    CONFIG_RESOURE_KEY = "config"

    def init(self, services):
        resource_service = services.get_service(Service_Key.RESOURCE)
        self.file_buffer = resource_service.get_resource(
            self.CONFIG_RESOURE_KEY)

    def start(self):
        self.config = RawConfigParser()
        self.config.read_file(self.file_buffer)

    def close(self):
        del self.config
        del self.file_buffer

    def get_config_value(self, section: str, option: str):
        return self.config.get(section, option)


class ConfigServiceFromArgs(Service):

    def init(self, services):
        self.config_args: dict = None
        self.services = services

    def start(self):
        self.config_args = {}

    def close(self):
        del self.config_args

    def set_args(self, **kwargs):
        self.config_args.update(kwargs)

    def get_config_value(self, key: str):
        return self.config_args.get(key)
