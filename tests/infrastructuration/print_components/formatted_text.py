import unittest

from pygments.token import Token

from infrastructuration.print_components.constant import PrintType
from infrastructuration.print_components.base import (
    BasePrintComponents,
    FormattedTextFactory,
)

class FormattedText(unittest.TestCase):

    def test_1_formatted_plain_text(self):
        type_ = PrintType.PLAIN_TEXT
        formatted_cls: BasePrintComponents = FormattedTextFactory().produce(type_)
        ins = formatted_cls()
        ins.type_context(context="Hello World")
        ins.to_print_formatted_text()
    
    def test_2_formatted_ansi_text(self):
        type_ = PrintType.FORMATTED_TEXT_ANSI
        formatted_cls: BasePrintComponents = FormattedTextFactory().produce(type_)
        ins = formatted_cls()
        ins.type_context(context="\x1b[31mhello \x1b[32mworld")
        ins.to_print_formatted_text()

    def test_3_formatted_html_text(self):
        type_ = PrintType.FORMATTED_TEXT_HTML
        formatted_cls: BasePrintComponents = FormattedTextFactory().produce(type_)
        ins = formatted_cls()
        ins.type_context(context="<a url='www.baidu.com'>hello world</a>")
        style_dict = {
            "a": "#44ff00 italic"
        }
        ins.wrapper_style(style_dict=style_dict)
        ins.to_print_formatted_text()

    def test_4_formatted_token_text(self):
        type_ = PrintType.FORMATTED_TEXT_TOKEN_TEXT
        formatted_cls: BasePrintComponents = FormattedTextFactory().produce(type_)
        ins = formatted_cls()
        contexts = ("hello", "world")
        ins.type_context(context=contexts)
        ins.wrapper_style(style_dict=(Token.Keyword, Token.Punctuation))
        ins.to_print_formatted_text()
    
    def test_5_formatted_style_text(self):
        type_ = PrintType.FORMATTED_TEXT_STYLE_TEXT
        formatted_cls: BasePrintComponents = FormattedTextFactory().produce(type_)
        ins = formatted_cls()
        contexts = [
            ("class:a", "hello"),
            ("class:b", "world"),
        ] 
        ins.type_context(context=contexts)
        style_dict = {
            "a": "#ff0066",
            "b": "#ff0066",
        }
        ins.wrapper_style(style_dict=style_dict)
        ins.to_print_formatted_text()
