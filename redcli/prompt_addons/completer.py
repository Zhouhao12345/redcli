import re
from typing import Iterable, Tuple

from prompt_toolkit.document import Document
from prompt_toolkit.completion import CompleteEvent, Completion, FuzzyCompleter, WordCompleter
from prompt_toolkit.completion.fuzzy_completer import _FuzzyMatch

from ..application.constant import Service
from ..application.app import app

logging_service = app.services.get_service(Service.LOGGER)
logger = logging_service.logging.getLogger(__name__)

redis_client = app.services.get_service(Service.REDIS)


class CustomWordCompleter(WordCompleter):

    def get_completions(
        self,
        document: Document,
        complete_event: CompleteEvent,
    ):
        texts = document.get_word_before_cursor()
        logger.info(f"Debug Log for Complete {texts}")
        if len(texts) >= 3:
            logger.info(f"Debug Log for Complete: {texts}")
            result_keys = redis_client.execute_method(
                "scan", match=f"*{texts}*", count=10)
            self.words = set(self.words) | set(result_keys[1])
        for word in self.words:
            yield Completion(
                text=word,
                start_position=0,
            )


class CustomFuzzyCompleter(FuzzyCompleter):

    def _get_fuzzy_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:

        word_before_cursor = document.get_word_before_cursor(
            pattern=re.compile(self._get_pattern())
        )

        completions = list(self.completer.get_completions(
            document, complete_event))

        fuzzy_matches: List[_FuzzyMatch] = []

        pat = ".*?".join(map(re.escape, word_before_cursor))
        # lookahead regex to manage overlapping matches
        pat = "(?=({0}))".format(pat)
        regex = re.compile(pat, re.IGNORECASE)
        for compl in completions:
            matches = list(regex.finditer(compl.text))
            if matches:
                # Prefer the match, closest to the left, then shortest.
                best = min(matches, key=lambda m: (m.start(), len(m.group(1))))
                fuzzy_matches.append(
                    _FuzzyMatch(len(best.group(1)), best.start(), compl)
                )

        def sort_key(fuzzy_match: "_FuzzyMatch") -> Tuple[int, int]:
            " Sort by start position, then by the length of the match. "
            return fuzzy_match.start_pos, fuzzy_match.match_length

        fuzzy_matches = sorted(fuzzy_matches, key=sort_key)

        for match in fuzzy_matches:
            # Include these completions, but set the correct `display`
            # attribute and `start_position`.
            yield Completion(
                match.completion.text,
                start_position=match.completion.start_position
                - len(word_before_cursor),
                display_meta=match.completion.display_meta,
                display=self._get_display(match, word_before_cursor),
                style=match.completion.style,
            )
