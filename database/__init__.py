from sqlite3.dbapi2 import SQLITE_READ
from .database_type import DatabaseType
from .dto import Task

from .file import FileDAO
from .sqlite import SqliteDAO
from settings import DBTYPE

dao = None
if DBTYPE == DatabaseType.FILE:
    dao = FileDAO()
elif DBTYPE == DatabaseType.SQLITE3:
    dao = SqliteDAO()
else:
    raise RuntimeError('DBTYPE: {} is invalid. Please check settings.py'.format(DBTYPE))