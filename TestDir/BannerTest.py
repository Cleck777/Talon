from typing import Callable, Dict, Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text, HTML, ANSI
from termcolor import colored

Banner = colored('''┏┓┳┓┏┓┏┓┓┏┓┏┓┏┳┓┏┓┏┳┓┳┏┓┳┓''', 'green') + '''\n'''
Banner += colored('''┃ ┣┫┣┫┃ ┃┫ ┗┓ ┃ ┣┫ ┃ ┃┃┃┃┃''', 'light_green') + '''\n'''
Banner += colored('''┗┛┛┗┛┗┗┛┛┗┛┗┛ ┻ ┛┗ ┻ ┻┗┛┛┗''', 'white') + '''\n'''
Banner += colored('''SUNY SOC''', 'white') + '''\n'''

print(Banner)
def 