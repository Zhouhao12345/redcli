from prompt_toolkit.buffer import Buffer
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion

from ..domain.adapters.redis import RedisAdapter


class CustomAutoSuggest(AutoSuggest):

    def get_suggestion(self, buffer: Buffer, document):
        suggest_map = RedisAdapter.get_suggest_map(version="5.7")
        text: str = buffer.text
        cmds = text.split(" ")
        if len(cmds) <= 1:
            return Suggestion('')
        args_sug = suggest_map.get(cmds[0], "")
        return Suggestion(args_sug)
