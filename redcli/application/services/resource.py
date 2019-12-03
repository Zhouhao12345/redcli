import os
from .base import Service

class ResourceService(Service):

    def init(self, services):
        self.resource_dir = [
            "redcli/resources",
        ]
        self.resource_map = {}

    def start(self):
        for dir_path in self.resource_dir:
            files = os.listdir(dir_path)
            for file_ in files:
                file_withoutext = os.path.splitext(file_)[0]
                self.resource_map.update({
                    file_withoutext: open(os.path.join(dir_path, file_)) 
                })

    def close(self):
        del self.resource_map
        del self.resource_dir


    def get_resource(self, key: str):
        return self.resource_map.get(key)
