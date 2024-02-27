from enum import IntEnum, StrEnum
import time
import math
import json

class ActivityType(StrEnum):
    PLAYING = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    CUSTOM = 4
    COMPETING = 5

class StatusType(IntEnum):
    ONLINE = "online"
    DO_NOT_DISTURB = "dnd"
    AFK = "idle"
    INVISIBLE = "invisible"
    OFFLINE = "offline"

class Activity(JSONSerializable):
    def __init__(self, name:str, atype:ActivityType=ActivityType.PLAYING, url:str=None, state:str=None):
        self.name:str = name
        self.type:ActivityType = atype
        self.url:str = url
        self.state:str = state
    def json(self):
        return {
                'type': self.type,
                'name': self.name,
                'url': self.url,
                'state': self.state
                }

class Presence(JSONSerializable):
    def __init__(self, since:int=None, activities:list[Activity], status:str=StatusType.ONLINE, afk:bool=False):
        self.activities:list[Activity] = activities
        self.afk = afk
        self.since = since
        self.status:str = (afk and StatusType.AFK) or status
    def json(self):
        return {'activities':self.activities,'afk':self.afk,'since':self.since,'status':self.status}
