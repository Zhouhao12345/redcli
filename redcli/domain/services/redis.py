from typing import List

from ..entity.redis import RedisEntity
from ..entity.operations import OperationEntity

class RedisService(object):

    @classmethod
    def get_all_operations(cls, version: str) -> List[str]:
        operations = RedisEntity(
            version=version
        ).get_operations()
        op_entities = []
        for operation in operations:
            op_entity = OperationEntity.load(operation)
            op_entities.append(op_entity.name)
        return op_entities
        
    @classmethod
    def get_suggest_map(cls, version: str) -> dict:
        operations = RedisEntity(
            version=version
        ).get_operations()
        op_entities = {}
        for operation in operations:
            op_entity = OperationEntity.load(operation)
            op_entities.update({
                op_entity.name: " ".join(op_entity.required_args)
            })
        return op_entities
        
