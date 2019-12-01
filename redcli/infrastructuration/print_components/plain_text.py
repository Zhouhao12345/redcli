from prompt_toolkit import print_formatted_text

from .constant import PrintType
from .base import BasePrintComponents

class PlainTextPrintComponents(BasePrintComponents):

    PRINT_TYPE = PrintType.PLAIN_TEXT

    def type_context(self, context: str):
        self.context = context

    def wrapper_style(self, style = None):
        pass

    def build_formatted_text(self) -> str:
        return self.context

    def to_print_formatted_text(self):
        print_formatted_text(self.context)
