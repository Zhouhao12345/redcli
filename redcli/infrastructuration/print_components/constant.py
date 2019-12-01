import enum

@enum.unique
class PrintType(str, enum.Enum):
    PLAIN_TEXT = "plain_text"
    FORMATTED_TEXT_HTML = "formatted_text_html"
    FORMATTED_TEXT_ANSI = "formatted_text_ansi"
    FORMATTED_TEXT_STYLE_TEXT = "formatted_text_style_text"
    FORMATTED_TEXT_TOKEN_TEXT = "formatted_text_token_text"
