# from prompt_toolkit import PromptSession

# # Create prompt object.
# session = PromptSession()
# text1 = None
# # Do multiple input calls.
# while text1 != "exit":
#     text1 = session.prompt()
#     print(f"response with result: {text1}")

from pygments.lexers.
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

html_completer = WordCompleter(['<html>', '<body>', '<head>', '<title>'])
text = prompt('Enter HTML: ', completer=html_completer, complete_while_typing=True)
print('You said: %s' % text)
