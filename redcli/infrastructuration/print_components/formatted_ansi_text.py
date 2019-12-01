from prompt_toolkit import (
    ANSI,
    print_formatted_text,
)

from .constant import PrintType
from .base import BasePrintComponents

class FormattedANSITextPrintComponents(BasePrintComponents):

    PRINT_TYPE = PrintType.FORMATTED_TEXT_ANSI

    def type_context(self, context: str):
        """context should be VT100 ANSI escape sequences  
        e.p: '\x1b[31mhello \x1b[32mworld'
        Parameters
        ----------
        context : str
            [description]
        """
        self.context = context

    def build_formatted_text(self) -> ANSI:
        return ANSI(self.context)

    def to_print_formatted_text(self):
        unformatted = self.build_formatted_text()
        print_formatted_text(unformatted)
