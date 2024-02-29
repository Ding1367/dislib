import os
from enum import IntEnum
from typing import *

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
    def __init__(self, type: int):
        self.type = type

class IdentifiedComponent(Component):
    def __init__(self, type: int, custom_id:Optional[str]=os.urandom(16).hex()):
        super().__init__(self, type)
        self.custom_id = custom_id

class CustomComponent:
    def __init__(self, type:int):
        self.type = type
        self._payload = {'type':self.type}
    def use_custom_id(self, id:Optional[str]=None):
        self.set_property(id or os.urandom(16).hex())
    def set_property(self, key: any, val: any):
        self._payload[key] = val
    def get_property(self, key: any):
        return self._payload[key]
    def payload(self):
        return self._payload
