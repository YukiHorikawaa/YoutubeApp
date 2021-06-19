from enum import Enum
from enum import IntEnum

class Key(Enum):
    TITLE = 'title'
    URL = 'url'
    DESCRIPTION = 'description'
    TAGS = 'tags'
class KeyNum(IntEnum):
    TITLE = 0
    URL = 1
    DESCRIPTION = 2
    TAGS = 3