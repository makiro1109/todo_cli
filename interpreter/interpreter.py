from .command import get_command
from .state import State
from .font_color import Color
import readline

def interpreter():
    state = State.NORMAL
    while not state == State.QUIT:
        try:
            print(Color.GREEN, end='')
            input_list = input('TODO> ').strip().split(None, 1)
            print(Color.RESET, end='')
            command_sym = ''
            if len(input_list) > 0:
                command_sym = input_list[0]
            args = ''
            if len(input_list) > 1:
                args = input_list[1]
            command = get_command(command_sym)
            state = command.execute(args)
        except KeyboardInterrupt:
            print('\nUse "quit" to quit.')
