import itertools as itl
#
# # lista donde guardamos los nombres de todas las clases definidas en el programa
# global_classes = []
# # diccionario key:(class_name,method_name) value: [args_types]
# class_methods_dict = {}


class Scope:

    scope_classes_dictionary = classes_dictionary

    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index_at_parent = 0 if parent is None else len(parent.locals)

    def define_variable(self, vname, vtypename):
        if vtypename not in self.scope_classes_dictionary:
            return None
        vtype = self.scope_classes_dictionary[vtypename]
        vinfo = VariableInfo(vname,vtype)
        if self.is_defined(vname):
            return None
        self.locals.append(vinfo)
        return vinfo

    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope

    def is_defined(self, vname):
        return self.get_variable_info(vname) is not None

    def get_variable_info(self, vname):
        current = self
        top = len(self.locals)
        while current is not None:
            vinfo = Scope.find_variable_info(vname, current, top)
            if vinfo is not None:
                return vinfo
            top = current.index_at_parent
            current = current.parent
        return None

    def is_local(self, vname):
        return self.get_local_variable_info(vname) is not None

    def get_local_variable_info(self, vname):
        return Scope.find_variable_info(vname, self)


    def _classes_global_field(self):
        return self.scope_classes_dictionary


    @staticmethod
    def find_variable_info(vname, scope, top=None):
        if top is None:
            top = len(scope.locals)
        candidates = (vinfo for vinfo in itl.islice(scope.locals, top) if vinfo.name == vname)
        return next(candidates, None)

    def get_type(self,typeName):
        if typeName not in self.scope_classes_dictionary:
            return None
        return self.scope_classes_dictionary[typeName]

    def get_type_for(self,symbol):
        '''
        Este metodo es el que busca el tipo de un id si está definido. Primero busca
        entre los atributos de la clase, luego entre los parametros del metodo que se está
        ejecutando y luego por las variables locales.
        Digo yo que es mejor definir primero en los nodos delos atributos a estos, luego
        en los nodos de los metodos se crean un scope nuevo y se agregan los parametros
        como nuevos simbolos.
        :param symbol:
        :return:
        '''

    def create_type(self,name,inherit_type_name):
        new_type = Type(name,parent_type=inherit_type_name)
        self.scope_classes_dictionary[name] = new_type

    def get_params_from_method(self, type_name, method_name):
        thetype = self.scope_classes_dictionary[type_name]
        if thetype is None:
            return None

        if method_name in thetype.methods:
            return thetype.methods[method_name]
        return None

    def get_type_from_attr(self,type_name,attr_name):
        thetype = self.scope_classes_dictionary[type_name]
        if thetype is None:
            return None

        if attr_name in thetype.attrs:
            return thetype.attrs[attr_name]
        return None


class VariableInfo:
    def __init__(self, name,vtype):
        self.name = name
        self.vmholder = None
        self.vtype = vtype

    def __eq__(self, other):
        return other.name == self.name

# a lo mejor sería buena idea hacer que se pueda instanciar una sola vez.
class Type:
    def __init__(self,name,attrs={},methods={},parent_type='Object'):
        self.name = name
        self.attrs = attrs
        self.methods = methods
        self._parent_type_name = parent_type
        self.parent_type = None
        self._checking_for_cycle = False
        self._checked_for_cycle = False

    def __eq__(self, other):
        return other.name == self.name

    def get_hierarchy_iterator(self):

        current_type = self
        object_obj = classes_dictionary['Object']
        while current_type != object_obj:
            yield current_type
            current_type = current_type.parent_type
        yield current_type

    def get_attr(self,name):
        '''
            Devuelve el attr con nombre name
            :param name: es un str con el nombre del atributo
            :return: Attr
            '''
        return self.attrs[name]

    def get_method(self,name):
        '''
            Devuelve el metodo con el identificador name
            :param name: name es un str del nombre del metodo a buscar
            :return: Method
            '''
        return self.methods[name]

    def get_lca(self, other_type):
        list_of_types = set()
        object_obj = classes_dictionary['Object']
        while other_type != object_obj:
            list_of_types.add(other_type)
            other_type = other_type.parent_type
        # Agregamos a la clase object
        list_of_types.add(other_type)

        parent_type = self
        while parent_type != object_obj:
            if parent_type in list_of_types:
                return parent_type
            parent_type = parent_type.parent_type
        return parent_type

    def define_attr(self,name,attr_type):
        '''
            Devuelve booleano
            :param name:
            :param type:
            :return:
            '''
        new_attr = Attrinfo(name,attr_type)
        self.attrs[name] = new_attr

    def define_parent(self,context):
        self.parent_type = context.scope_classes_dictionary[self._parent_type_name]

    def define_method(self,name,return_type,arguments=[]):
        '''
            Devuelve un booleano
            :param name:
            :param return_type:
            :param arguments:
            :return:
            '''
        new_method = Methodinfo(name,return_type,arguments)
        self.methods[name] = new_method

# en este diccionario se va a mapear el nombre del tipo
# a la instancia del mismo que contendrá todos sus metodos y attributos
classes_dictionary = {'Int':Type('Int'),
                      'String':Type('String'),
                      'Bool':Type('Bool'),
                      'Object':Type('Object',parent_type=None)
                      }

class Attrinfo:
    def __init__(self,name,attr_type):
        self.name = name
        self.type = attr_type

    def __eq__(self, other):
        return other.name == self.name

class Methodinfo:
    def __init__(self,name,return_type,arguments=[]):
        self.name = name
        self.return_type = return_type
        self.arguments = arguments

    def __eq__(self, other):
        return other.name == self.name and \
               len(other.arguments) == len(self.arguments)

class ErrorLogger:
    def log_error(self,mesagge):
        pass