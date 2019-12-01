from ..services.redis import RedisService

class RedisAdapter(object):

    @classmethod
    def get_operations(cls, version: str) -> list:
        return RedisService.get_all_operations(version=version)

    @classmethod
    def get_suggest_map(cls, version: str) -> dict:
        return RedisService.get_suggest_map(version=version)
        
