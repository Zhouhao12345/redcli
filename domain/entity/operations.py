from typing import Callable, List
import inspect
import dataclasses

@dataclasses.dataclass
class OperationEntity(object):
    name: str = None
    help_message: str = None
    required_args: List[str] = None

    @classmethod
    def load(cls, func: Callable):
        full_args = inspect.getfullargspec(func)
        required_args = [ _ for _ in full_args.args if _ not in (
            'self', 'cls'
        )]
        return cls(
            name=func.__name__,
            help_message=func.__doc__,
            required_args=required_args,
        )
