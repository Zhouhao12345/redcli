from typing import Union, Callable, List, Optional, Dict

from pprint import pformat
import click
import redis
from redis import RedisError

import pygments
from pygments.token import Token
from pygments.lexers.python import PythonLexer

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import ThreadedCompleter
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit import print_formatted_text

from .domain.adapters.redis import RedisAdapter


@click.command()
@click.option("-H", "--host", default="localhost", type=str, help="redis host name")
@click.option("-P", "--port", default="6379", type=int, help="redis port")
@click.option("-p", "--password", default=None, type=str, help="redis password")
@click.option("-d", "--database", default=0, type=int, help="redis database")
def redcli(host: str, port: int, password: str, database: int):
    from .application.constant import Service as Service_e
    from .application.app import app
    from .application.services import (
        config,
        redis as redis_s,
    )
    app.init()
    config_args_service = config.ConfigServiceFromArgs()
    app.services.register_service(
        Service_e.CONFIG_ARGS, config_args_service)
    config_args_service.set_args(
        host=host,
        port=port,
        password=password,
        db=database,
        decode_responses=True,
    )
    redis_c = redis_s.RedisService()
    app.services.register_service(
        Service_e.REDIS, redis_c
    )

    from .prompt_addons.completer import CustomWordCompleter, CustomFuzzyCompleter
    from .prompt_addons.suggestion import CustomAutoSuggest

    globals_style_dict = {
        'synax': "aqua bold",
        'host':  "aqua bold",
        'port':  "aqua bold",
        "result": "white bold",
    }
    help_prefix = [
        ("class:host", host),
        ("class:synax", "@"),
        ("class:port", str(port)),
        ("class:synax", ": "),
    ]
    exit_commands = ('exit', 'q', 'exit()')

    global_style = Style.from_dict(globals_style_dict)
    all_ops = RedisAdapter.get_operations(version="5.7")
    session = PromptSession()

    command = None
    # Do multiple input calls.
    while True:
        command = session.prompt(
            message=help_prefix,
            style=global_style,
            completer=ThreadedCompleter(CustomFuzzyCompleter(
                CustomWordCompleter(words=all_ops))),
            auto_suggest=CustomAutoSuggest(),
            complete_in_thread=True,
        )
        if command in exit_commands:
            break
        try:
            result = str(redis_c.execute_command(command))
        except RedisError as e:
            result = str(e)
        tokens = list(pygments.lex(result, lexer=PythonLexer()))
        print_formatted_text(PygmentsTokens(tokens))


if __name__ == "__main__":
    redcli()
