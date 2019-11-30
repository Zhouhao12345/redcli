from typing import Callable

import inspect
import redis
import dataclasses

@dataclasses.dataclass
class RedisEntity(object):

    version: str = None

    @classmethod
    def func_filter(cls, key: str) -> bool:
        if not key.startswith("_") and not key.startswith("__") and key.islower():
            return True

    def get_operations(self) -> Callable:
        all_memb_map =  dict(inspect.getmembers(redis.StrictRedis))
        return [
            _ for key, _ in all_memb_map.items() if self.func_filter(key)
        ]
