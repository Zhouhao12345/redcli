from typing import Dict, OrderedDict
from collections import OrderedDict as OrderedDict_d
from abc import ABC, abstractmethod


class Service(ABC):

    @abstractmethod
    def init(self, services):
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError


class Services(object):

    def init(self):
        self.services: OrderedDict[str, Service] = OrderedDict_d()

    def get_service(self, service_name: str) -> Service:
        return self.services.get(service_name)

    def register_service(self, service_name: str, service: Service):
        service.init(self)
        service.start()
        self.services.update({
            service_name: service
        })

    def close_service(self, service_name: str):
        service = self.services.get(service_name)
        if service:
            service.close()

    def close(self):
        for service in self.services:
            service.close()
