import enum


@enum.unique
class Service(str, enum.Enum):
    LOGGER = "logger"
    CONFIG_LOCAL = "config_local"
    CONFIG_ARGS = "config_args"
    RESOURCE = "resource"
    REDIS = "redis"
