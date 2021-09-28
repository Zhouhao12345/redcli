from prompt_toolkit import (
    HTML,
    print_formatted_text,
)

from .constant import PrintType
from .base import BasePrintComponents

class FormattedHtmlTextPrintComponents(BasePrintComponents):

    PRINT_TYPE = PrintType.FORMATTED_TEXT_HTML

    def type_context(self, context: str):
        """context should be html text
        
        Parameters
        ----------
        context : str
            [description]
        """
        self.context = context

    def wrapper_style(self, style_dict: dict):
        """html style, css style for each html tags
        e.p:
        style dict should be {
            "a": "#ff0066"
        }
        unformatted text should be "<a>test text</a>"
        Parameters
        ----------
        styple : [type], optional
            [description], by default None
        """
        super(FormattedHtmlTextPrintComponents, self).wrapper_style(
            style_dict)


    def build_formatted_text(self) -> HTML:
        return HTML(self.context)

    def to_print_formatted_text(self):
        unformatted = self.build_formatted_text()
        print_formatted_text(unformatted, style=self.style)
