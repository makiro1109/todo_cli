from .command import get_command
from .state import State
from .font_color import Color
import readline

def interpreter():
    state = State.NORMAL
    while not state == State.QUIT:
        try:
            print(Color.GREEN, end='')
            input_list = input('TODO> ' + Color.RESET).strip().split(None, 1)
            input_iter = iter(input_list)
            cmd_sym = next(input_iter, '')
            args    = next(input_iter, '')
            command = get_command(cmd_sym)
            state = command.execute(args)
        except KeyboardInterrupt:
            print('\nUse "quit" to quit.')
