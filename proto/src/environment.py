
class Env(object):
    def __init__(self, variables=None, functions=None, modules=None, parent=None):
        self.parent = parent
        self.variables = variables or {} # Store nested dicts as "name": {"type": type, "value": value}
        self.functions = functions or {}
        if modules is not None:
            self.modules = modules
        elif parent is not None:
            self.modules = parent.modules   # share registry
        else:
            self.modules = {}

    def define(self, name, value):
        self.variables[name] = value
        
class ModuleEnv(Env):
    def __init__(self, module_name, variables=None, functions=None, modules=None, parent=None):
        super().__init__(variables=variables, functions=functions, modules=modules, parent=parent)
        self.module_name = module_name 