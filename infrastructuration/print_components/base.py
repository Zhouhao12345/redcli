from __future__ import absolute_import, annotations

import typing
from typing import (
    Tuple,
    Dict,
    List,
    Union, 
)

from abc import (
    ABC,
    abstractmethod,
)
from prompt_toolkit import print_formatted_text
from prompt_toolkit.styles import (
    Style,
)
if typing.TYPE_CHECKING:
    from pygments.token import _TokenType
    from prompt_toolkit import (
        ANSI,
        HTML,
    )
    from prompt_toolkit.formatted_text import (
        FormattedText,
        PygmentsTokens,
    )

class BasePrintComponents(ABC):

    PRINT_TYPE = None

    @abstractmethod
    def type_context(self, context: Union[
        str,
        List[Tuple[str]]
    ]):
        raise NotImplementedError

    def wrapper_style(self, style_dict: Union[Dict, List[_TokenType]]):
        self.style = Style.from_dict(style_dict)

    @abstractmethod
    def build_formatted_text(self) -> Union[
        FormattedText, 
        PygmentsTokens, 
        HTML, 
        ANSI,
        str,
    ]:
        raise NotImplementedError

    @abstractmethod
    def to_print_formatted_text(self):
        raise NotImplementedError

class FormattedTextFactory(object):

    def __init__(self):
        from infrastructuration.print_components.plain_text import PlainTextPrintComponents
        from infrastructuration.print_components.formatted_ansi_text import FormattedANSITextPrintComponents
        from infrastructuration.print_components.formatted_html_text import FormattedHtmlTextPrintComponents
        from infrastructuration.print_components.formatted_style_text import FormattedStyleTextPrintComponents
        from infrastructuration.print_components.formatted_token_text import FormattedTokenTextPrintComponents 

    def produce(self, formatted_type: str) -> BasePrintComponents:
        for sub_cls in BasePrintComponents.__subclasses__():
            if sub_cls.PRINT_TYPE == formatted_type:
                return sub_cls
