from typing import List, Tuple

from prompt_toolkit import (
    print_formatted_text,
)
from prompt_toolkit.formatted_text import (
    FormattedText
)

from .constant import PrintType
from .base import BasePrintComponents


class FormattedStyleTextPrintComponents(BasePrintComponents):

    PRINT_TYPE = PrintType.FORMATTED_TEXT_STYLE_TEXT

    def type_context(self, context: List[Tuple[str]]):
        """context should be list of tuple with class name and unformatted text  
        e.p: [("class:aa": "hello"),("class:bb": "world")] 
        Parameters
        ----------
        context : List 
            [description]
        """
        self.context = context

    def wrapper_style(self, style_dict: dict):
        """html style, css style for each html tags
        e.p:
        style dict should be {
            "aa": "#ff0066"
            "bb": "#ff0066"
        }
        Parameters
        ----------
        styple : [type], optional
            [description], by default None
        """
        super(FormattedStyleTextPrintComponents, self).wrapper_style(
            style_dict)

    def build_formatted_text(self) -> FormattedText:
        return FormattedText(self.context)

    def to_print_formatted_text(self):
        unformatted = self.build_formatted_text()
        print_formatted_text(unformatted, style=self.style)
