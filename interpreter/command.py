import re
import readline
from datetime import datetime, timedelta
from .state import State
from .font_color import Color
from database import dao, Task
from consts import DATETIME_MAX

commands = []

def parse_arguments(args):
    arg_vals = {'shorts': ''}
    if len(args) == 0:
        return arg_vals
    long_pattern = r'--(\w+)=("([^"]*)"|(\S*))'
    short_pattern = r'(\s|^)-(\w+)'
    for result in re.findall(short_pattern, args):
        arg_vals['shorts'] += result[1]
    for result in re.findall(long_pattern, args):
        arg_vals[result[0]] = result[2] if result[2] != '' else result[3]
    return arg_vals

def parse_id(id_str):
    if id_str is None:
        raise ValueError('--id option required.')
    try:
        task_id = int(id_str)
    except ValueError:
        raise ValueError('Invalid value: "{}"'.format(id_str))
    return task_id

def get_task_by_taskid(id_str):
    try:
        task_id = parse_id(id_str)
        task = dao.select({'id': task_id})
    except ValueError as e:
        raise e
    except StopIteration:
        raise ValueError('Task not found: {}'.format(id_str))
    return task

def set_options(task, args):
    if args.get('title'):
        task.title = args.get('title')
    if args.get('note'):
        task.note = args.get('note')
    if args.get('done'):
        if args.get('done') == 'True':
            task.is_done = True
        elif args.get('done') == 'False':
            task.is_done = False
        else:
            raise ValueError('Specify done option as "True" or "False"')
    if args.get('deadline'):
        try:
            task.deadline = datetime.strptime(args['deadline'], '%Y/%m/%d %H:%M:%S')
        except ValueError:
            raise ValueError('input datetime like "year/month/date hour:minute:second')
    return task

class Command:
    symbol = ''
    usage = ''
    short_options = []
    long_options = []
    def execute(self, args):
        print('unimplemented!')
        return State.NORMAL

class Nap(Command):
    """for enter only"""
    def execute(self, args):
        return State.NORMAL

commands.append(Nap())

class Show(Command):
    symbol = 'show'
    usage = 'Show registered tasks.'
    short_options = [
        ('a', 'show all tasks.'),
        ('s', 'sort by deadline')]
    def execute(self, args):
        args = parse_arguments(args)
        params = {}
        params['all'] = True if 'a' in args['shorts'] else False
        tasks = dao.select(params)
        if 's' in args['shorts']:
            tasks = sorted(tasks, key=lambda t: t.deadline)
        for task in tasks:
            if task.is_done:
                print(Color.LIGHT, end='')
            elif task.deadline < datetime.now():
                print(Color.RED, end='')
            elif task.deadline < datetime.now() + timedelta(days=1):
                print(Color.YELLOW, end='')
            
            print(Color.UNDERLINE, Color.BOLD, end='')
            print('{}: {}'.format(task.id, task.title))
            print(Color.RM_UNDERLINE, end='')

            if (task.deadline != DATETIME_MAX):
                print('  deadline: {}'.format(task.deadline))
            if (task.note != ''):
                print('  note: {}'.format(task.note))
            print(Color.RESET, end='')
        
commands.append(Show())

class Delete(Command):
    symbol = 'delete'
    usage = 'Delete task.'
    long_options = [
        ('id', '(required) set id number.')]
    def execute(self, args):
        args = parse_arguments(args)
        try:
            task_id = parse_id(args.get('id'))
        except ValueError as e:
            print(e)
            return State.ERROR
        if dao.delete(task_id):
            print('Task id: {} deleted.'.format(task_id))
        else:
            print('Task not found: {}'.format(task_id))
        return State.NORMAL

commands.append(Delete())

class Add(Command):
    symbol = 'add'
    usage = ''
    long_options = [
        ('title',    'set task title.'),
        ('deadline', 'set task deadline.'),
        ('note ',     'set task note.'),
    ]
    def execute(self, args):
        args = parse_arguments(args)
        task = Task()
        try:
            set_options(task, args)
        except ValueError as e:
            print(e)
            return State.ERROR
        dao.insert({'task': task})
        return State.NORMAL

commands.append(Add())

class Update(Command):
    symbol = 'update'
    usage = ''
    long_options = [
        ('id', '(required) set id number.'),
        ('title',    'set task title.'),
        ('deadline', 'set task deadline.'),
        ('note ',    'set task note.'),
        ('done',     'set task is done.')
    ]
    def execute(self, args):
        args = parse_arguments(args)
        try:
            task = get_task_by_taskid(args.get('id'))
            set_options(task, args)
        except ValueError as e:
            print(e)
            return State.ERROR
        task.update_at = datetime.now()
        if dao.update(task):
            print('update was successfull')
        else:
            print('Task not found')
        return State.NORMAL

commands.append(Update())

class Done(Update):
    symbol = 'done'
    usage = 'Complete a task'
    long_options = [
        ('id', '(required) set id number.')]
    def execute(self, args):
        args += ' --done=True'
        return super().execute(args)

commands.append(Done())

class Restart(Update):
    symbol = 'restart'
    usage = 'Restart a task'
    long_options = [
        ('id', '(required) set id number.')]
    def execute(self, args):
        args += ' --done=False'
        return super().execute(args)

commands.append(Restart())

class Quit(Command):
    symbol = 'quit'
    usage = 'Quit this application.'
    def execute(self, args):        
        print('Bye.')
        return State.QUIT

commands.append(Quit())

class Exit(Quit):
    symbol = 'exit'
    usage = 'Alias of quit.'

commands.append(Exit())

class Help(Command):
    symbol = 'help'
    usage = 'Print this help message.'
    def execute(self, args):
        for command in filter(lambda x: x.symbol != '', commands):
            print('{}: {}'.format(command.symbol, command.usage))
            for param in command.short_options:
                print(' -{}\t{}'.format(*param))
            for param in command.long_options:
                print(' --{}\t{}'.format(*param))
        return State.NORMAL

commands.append(Help())

class Unknown():
    def __init__(self, symbol):
        self.symbol = symbol

    def execute(self, args):
        print('Command "{}" not found.'.format(self.symbol))
        print('Execute "help" to list commands.')
        return State.NORMAL

def get_command(symbol):
    command = next(
        filter(lambda x: x.symbol == symbol, commands),
        Unknown(symbol))
    return command

