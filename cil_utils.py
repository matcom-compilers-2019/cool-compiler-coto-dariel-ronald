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
