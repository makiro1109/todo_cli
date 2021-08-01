from .database_type import DatabaseType
from .dto import Task

from settings import DBTYPE
from .file import FileDAO

dao = None
if DBTYPE == DatabaseType.FILE:
    dao = FileDAO()
else:
    raise RuntimeError('DBTYPE: {} is invalid. Please check settings.py'.format(DBTYPE))