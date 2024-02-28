import os
from enum import IntEnum

class ComponentType(IntEnum):
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_STRING = 3
    TEXT_INPUT = 4
    SELECT_USER = 5
    SELECT_ROLE = 6
    SELECT_MENTION = 7
    SELECT_CHANNEL = 8

class Component:
    type: int
    def __init__(self, type: int):
        self.type = type

class CustomComponent(Component):
    def __init__(self, custom_id:str=None, type: int):
        super().__init__(self, type)
        if not custom_id:
            custom_id = os.urandom(16).hex()
        self.custom_id = custom_id

class ActionRow(Component):
    def __init__(self):
        super().__init__(self, ComponentType.ACTION_ROW)
