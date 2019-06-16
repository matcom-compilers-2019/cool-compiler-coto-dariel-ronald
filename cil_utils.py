import itertools as itl
class Cil_Type:
    def __init__(self,name,attributes = [], methods = []):
        self.name= name
        self.attributes = attributes
        self.methods = methods

class Cil_Data:
    def __init__(self, id, value):
        self.id = id
        self.value = value

class Cil_Code:
    def __init__(self,functions = []):
        self.functions = functions

class Cil_Function:
    def __init__(self, args = [], localva = [], instructions = []):
        self.args = args
        self.locals = localva
        self.instructions = instructions


class CILScope:

    def __init__(self, parent=None):
        self.locals = {}
        self.parent = parent
        self.children = []
        # self.index_at_parent = 0 if parent is None else len(parent.locals)

    def define_variable(self, vname, alias):
        if self.is_defined(vname):
            return None
        self.locals[vname] = alias
        return alias

    def get_locals(self):
        locals_results = []

        current = self
        while current is not None:
            locals_results += list(current.locals.values())
            current = current.parent
        return locals_results

    def create_child_scope(self):
        child_scope = CILScope(self)
        self.children.append(child_scope)
        return child_scope

    def is_defined(self, vname):
        return self.get_variable_alias(vname) is not None

    def get_variable_alias(self, vname):
        current = self
        while current is not None:
            alias = self.locals[vname] if vname in self.locals else None
            if alias is not None:
                return alias
            current = current.parent
        return None
