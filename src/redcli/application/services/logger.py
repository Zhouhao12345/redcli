from ..constant import Service as Service_Key
from .base import Service
import logging

class LoggerService(Service):

    def init(self, services):
        config_service = services.get_service(Service_Key.CONFIG_LOCAL)
        self.date_format = config_service.get_config_value(
            "LOGGER", "DateFormat")
        self.format_str = config_service.get_config_value(
            "LOGGER", "FormatString"
        )
        level_str = config_service.get_config_value(
            "LOGGER", "LEVEL"
        )
        self.level = getattr(logging, level_str)
        self.file_path = config_service.get_config_value(
            "LOGGER", "FilePath"
        )

    def start(self):
        self._logging = logging
        self._logging.basicConfig(
            filename=self.file_path,
            level=self.level,
            filemode="w",
            format=self.format_str,
            datefmt=self.date_format,
        )
    
    def close(self):
        del self._logging
        del self.file_path
        del self.level
        del self.format_str
        del self.date_format

    @property
    def logging(self):
        return self._logging
