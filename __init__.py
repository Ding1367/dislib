from .ui import *
from .bot import *
from .snowflake import *
import json

DISCORD_EPOCH = 1420070400000

class JSONSerializable:
    def __init___(self): pass
    def json(self): pass
    def __str__(self): return json.dumps(self.json())

class NotIndexable(RuntimeError):
    def __init__(self, inst):
        super().__init__(self, f'Instance {inst} is not indexable')

def convert_classes(obj):
    if hasattr(obj, 'payload'):
        obj = obj.payload()
    for x in (isinstance(obj, dict) and obj.keys()) or (isinstance(obj, list) and obj) or raise NotIndexable(obj):
        if hasattr(obj[x], 'payload'):
            obj[x] = convert_classes(obj[x])
    return obj
