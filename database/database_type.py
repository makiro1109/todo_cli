from enum import Enum, auto

class DatabaseType(Enum):
    SQLITE3 = auto()
    FILE    = auto()
