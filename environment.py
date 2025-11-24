
class Env(object):
    def __init__(self, variables=None, functions=None, parent=None):
        self.variables = variables or {} # Store nested dicts as "name": {"type": type, "value": value}
        self.functions = functions or {}
        self.parent = parent or None

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)  # walk up the parent chain
        else:
            raise NameError(f"Variable {name} not found (method:get)")

    def set(self, name, value):
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.set(name, value)  # update in the defining env
        else:
            raise NameError(f"Variable {name} not found (method:set)")