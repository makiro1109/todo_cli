import os
import sys
from shutil import copyfile
from datetime import datetime
from .consts import FILEDB_FILEPATH as DBFILEPATH
from ..dto import Task

def line_to_task(idx, line):
    data_iter = iter(line.split(','))
    task = None
    try:
        task = Task(
            id = idx,
            title = next(data_iter),
            deadline = datetime.fromtimestamp(float(next(data_iter))),
            note = next(data_iter),
            is_done = True if next(data_iter) == 'True' else False,
            create_at = datetime.fromtimestamp(float(next(data_iter))),
            update_at = datetime.fromtimestamp(float(next(data_iter)))
        )
    except:
        print('Error: Invalid record. Check {}.'.format(DBFILEPATH))
        sys.exit(1)
    return task

def task_to_line(task):
    strs = [
        task.title,
        str(task.deadline.timestamp()),
        task.note,
        str(task.is_done),
        str(task.create_at.timestamp()),
        str(task.update_at.timestamp()),
    ]
    return ','.join(strs)

def reader(filepath):
    idx = 1
    with open(filepath, mode='r', encoding='utf-8') as f:
        for line in filter(lambda x: x != '\n', f):
            yield line_to_task(idx, line)
            idx += 1

def append(filepath, txt):
    with open(filepath, mode='a', encoding='utf-8') as f:
        f.write('\n' + txt)

class FileDAO:
    """
    DatabaseType == FILE の時に用いるDAO
    """
    def select_all(self):
        return reader(DBFILEPATH)

    def select_not_done(self):
        return filter(
            lambda task: not task.is_done,
            reader(DBFILEPATH))
    
    def select_by_id(self, id):
        return next(
            (t for t in reader(DBFILEPATH) if t.id == id))

    def select(self, params):
        if params.get('all'):
            return self.select_all()
        if params.get('id') is not None:
            return self.select_by_id(params.get('id'))
        else:
            return self.select_not_done()

    def insert(self, params):
        append(DBFILEPATH, task_to_line(params['task']))

    def update(self, task):
        tmpfile = DBFILEPATH + '.tmp'
        is_updated = False
        # TODO: self.appendで書き直してみて速度の違いを見たい
        with open(tmpfile, 'w') as f:
            for t in self.select_all():
                if t.id == task.id:
                    is_updated = True
                    target = task
                else:
                    target = t
                f.write(task_to_line(target) + '\n')
        copyfile(tmpfile, DBFILEPATH)
        os.remove(tmpfile)
        return is_updated

    def delete(self, id):
        tmpfile = DBFILEPATH + '.tmp'
        is_deleted = False
        with open(tmpfile, 'w') as f:
            for t in self.select_all():
                if t.id == id:
                    is_deleted = True
                    continue
                f.write(task_to_line(t) + '\n')
        copyfile(tmpfile, DBFILEPATH)
        os.remove(tmpfile)
        return is_deleted

