from enum import IntEnum
from typing import *
import os

class UrlButtonWithoutUrlError(RuntimeError):
    def __init__(self):
        super().__init__(self, "Button of style 5 (LINK) without 'url'")

class ButtonStyle(IntEnum):
    PRIMARY = 1
    blurple = 1

    SECONDARY = 2
    grey = 2
    gray = 2

    SUCCESS = 3
    green = 3
    
    DANGER = 4
    red = 4

    LINK = 5

class Button(Component):
    def __init__(self, label:str, style:Optional[int]=ButtonStyle.blurple, disabled:Optional[bool]=False, custom_id:Optional[str]=None, url:Optional[bool]=None):
        super().__init__(self, ComponentType.BUTTON)
        self.label = label
        self.style = style
        self.disabled = disabled
        if style != ButtonStyle.LINK:
            self.custom_id = custom_id or os.urandom(16).hex()
        elif style == ButtonStyle.LINK:
            if not url:
                raise UrlButtonWithoutUrlError()
            self.url = url
    def payload(self):
        return {'type':ComponentType.BUTTON,'label':self.label,'style':self.style,'custom_id':self.custom_id,'url':self.url, 'disabled':self.disabled}
