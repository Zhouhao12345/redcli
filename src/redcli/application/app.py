from .constant import Service as Service_keys
from .services.base import Services
from .services import (
    resource,
    config,
    logger,
)


class Application(object):

    def __init__(self):
        self.services = Services()
        self.services.init()

    def init(self):
        services_tuple = (
            (Service_keys.RESOURCE, resource.ResourceService),
            (Service_keys.CONFIG_LOCAL, config.ConfigServiceLocal),
            (Service_keys.LOGGER, logger.LoggerService),
        )
        for key, service in services_tuple:
            self.services.register_service(key, service())


app = Application()
