from __future__ import absolute_import, annotations
from typing import (
    List, 
    Tuple,
    TYPE_CHECKING,
)

from prompt_toolkit import (
    print_formatted_text,
)
from prompt_toolkit.formatted_text import (
    PygmentsTokens 
)

from .constant import PrintType
from .base import BasePrintComponents

if TYPE_CHECKING:
    from pygments.token import _TokenType

class FormattedTokenTextPrintComponents(BasePrintComponents):

    PRINT_TYPE = PrintType.FORMATTED_TEXT_TOKEN_TEXT

    def type_context(self, context: List[str]):
        """context should be list of str, splited by specific style  
        e.p: ("hello", "world") 
        Parameters
        ----------
        context : List 
            [description]
        """
        self.context = context

    def wrapper_style(self, style_dict: List[_TokenType]):
        """ List of pygments tokens
        e.p:
        style dict should be  (Token.Keyword, Token.Punctuation)       
        
        Parameters
        ----------
        styple : [type], optional
            [description], by default None
        """
        self.style_tokens = style_dict


    def build_formatted_text(self) -> FormattedText:
        assert len(self.context), len(self.style_tokens)
        ziped_list = [_ for _ in zip(self.style_tokens, self.context)]
        return PygmentsTokens(ziped_list) 

    def to_print_formatted_text(self):
        unformatted = self.build_formatted_text()
        print_formatted_text(unformatted)
