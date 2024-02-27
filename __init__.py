import json

class JSONSerializable:
    def __init___(self): pass
    def json(self): pass
    def __str__(self): return json.dumps(self.json())
