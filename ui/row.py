class RowInRowError(RuntimeError):
    def __init__(self):
        super().__init__(self, "An action row cannot contain an action row.")

class ActionRow(Component):
    def __init__(self,components:Optional[List[Component]]=[]):
        super().__init__(self, ComponentType.ACTION_ROW)
        if components:
            for idx in components:
                components[idx] = components[idx].payload()
        self._components = []
    def add(self, comp:Component):
        if isinstance(comp, ActionRow):
            raise RowInRowError()
        self._components.append(comp)
    def payload(self):
        return {'type': self.type, 'components': convert_classes(self._components)}
