from typing import *
import os

class SelectMenu(IdentifiedComponent):
    def __init__(self, type:int, custom_id:Optional[str]=os.urandom(16).hex(), disabled:Optional[bool]=False, placeholder:Optional[str]=None,min:Optional[int]=1,max:Optional[int]=1):
        super().__init__(self, type, custom_id)
        self.disabled = disabled
        self.placeholder = placeholder
        self.min = min
        self.max = max

class StringSelectOption:
    def __init__(self, label: str, value:Optional[str]=None, description:Optional[str]=None, default:Optional[bool]=False):
        self.label = label
        self.value = value or label
        self.description = description
        self.default = default
    def payload(self):
        return {'label':self.label, 'value':self.value, 'description':self.description,'default':self.default}

class StringSelectMenu(SelectMenu):
    def __init__(self, options:List[StringSelectOption], custom_id:Optional[str]=None, placeholder:Optional[str]=None, min:Optional[int]=None, max:Optional[int]=None):
        super().__init__(self, ComponentType.SELECT_STRING, custom_id, disabled, placeholder, min, max)
        self.options = options
    def payload(self):
        return {'disabled':self.disabled,'placeholder':self.placeholder,'options':convert_classes(options),'custom_id':self.custom_id,'type':self.type,'min':self.min,'max':self.max}




