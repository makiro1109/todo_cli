import sqlite3


class SqliteDAO:
    def __init__(self):
        self.con = sqlite3.connect('t_task')

    def select(self, params):
        pass

    def insert(self, params):
        pass

    def update(self, params):
        pass

    def delete(self, params):
        pass