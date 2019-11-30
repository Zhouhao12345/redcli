# from prompt_toolkit import PromptSession

# # Create prompt object.
# session = PromptSession()
# text1 = None
# # Do multiple input calls.
# while text1 != "exit":
#     text1 = session.prompt()
#     print(f"response with result: {text1}")
from typing import Union, Callable, List, Optional, Dict
import click
import redis
from redis import RedisError
from prompt_toolkit import prompt
from prompt_toolkit.document import Document
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.buffer import Buffer, BufferEventHandler
from prompt_toolkit.styles import Style

from prompt_toolkit.completion import FuzzyWordCompleter, FuzzyCompleter, Completer, WordCompleter, CompleteEvent
from prompt_toolkit import PromptSession

from infrastructuration.print_components.formatted_style_text import FormattedStyleTextPrintComponents
from domain.adapters.redis import RedisAdapter
globals_style_dict =  {
    'synax': "#ffffff bold",
    'host':   '#888888 bold',
    'port':   '#ff88ff bold',
    "result": '#555555 bold',
}

global_style = Style.from_dict(globals_style_dict)

exit_commands = ('exit', 'q', 'exit()')



# Create prompt object.
session = PromptSession()

all_ops = RedisAdapter.get_operations(version="5.7")
suggest_map = RedisAdapter.get_suggest_map(version="5.7")


class CustomWordCompleter(WordCompleter):

    def get_completions(
        self, 
        document: Document, 
        complete_event: CompleteEvent,
    ):
        texts = document.text_before_cursor.split(" ")
        if len(texts) >= 2:
            after_text = "".join(texts[1:-1])
            result_keys = self.redis_client.scan(cursor=0, match=f"*{after_text}*", count=10)
            if result_keys:
                self.words.extend([_ for _ in result_keys[1] if _ not in self.words])
        return super(CustomWordCompleter, self).get_completions(document, complete_event)


class CustomFuzzyWordCompleter(FuzzyWordCompleter):

    def __init__(
        self,
        words: Union[List[str], Callable[[], List[str]]],
        redis_client: redis.StrictRedis,
        meta_dict: Optional[Dict[str, str]] = None,
        WORD: bool = False,
    ) -> None:

        self.words = words
        self.meta_dict = meta_dict or {}
        self.WORD = WORD

        self.word_completer = CustomWordCompleter(
            words=self.words, WORD=self.WORD, meta_dict=self.meta_dict
        )
        self.word_completer.redis_client = redis_client

        self.fuzzy_completer = FuzzyCompleter(self.word_completer, WORD=self.WORD)



def get_cmd_back_args(buffer: Buffer):
    pass

class CustomAutoSuggest(AutoSuggest):

    def get_suggestion(self, buffer: Buffer, document):
        text: str = buffer.text
        cmds = text.split(" ")
        if len(cmds) <= 1:
            return Suggestion('')
        args_sug = suggest_map.get(cmds[0], "")
        return Suggestion(args_sug)


@click.command()
@click.option("-H", "--host", default="localhost", type=str, help="redis host name")
@click.option("-P", "--port", default="6379", type=int, help="redis port")
@click.option("-p","--password", default=None, type=str, help="redis password")
@click.option("-d", "--database", default=0, type=int, help="redis database")
def redcli(host: str, port:int, password:str, database: int):
    help_prefix = [
        ("class:host", host),
        ("class:synax", "@"),
        ("class:port", str(port)),
        ("class:synax", ": "),
    ]
    redis_client = redis.StrictRedis(host=host, port=port, password=password, db=database, decode_responses=True)
    comp =  CustomFuzzyWordCompleter(words=all_ops, redis_client=redis_client)
    command = None
    # Do multiple input calls.
    while True: 
        command = session.prompt(
            message=help_prefix, 
            style=global_style,
            completer=comp,
            auto_suggest=CustomAutoSuggest(),
        )
        if command in exit_commands:
            break
        try:
            result = str(redis_client.execute_command(command))
        except RedisError as e:
            result = str(e)
        response = FormattedStyleTextPrintComponents()
        response.type_context(
            [
                ("class:synax", ":"),
                ("class:result", result)
            ]
        )
        response.wrapper_style(style_dict=globals_style_dict)
        response.to_print_formatted_text()

if __name__ == "__main__":
    redcli()     