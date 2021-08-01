from consts import DATETIME_MAX
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    """
    Class for keeping track of a task.
    """
    id: int = 0
    title: str = ''
    note: str = ''
    is_done: bool = False
    deadline:  datetime = DATETIME_MAX
    create_at: datetime = datetime.now()
    update_at: datetime = datetime.now()
