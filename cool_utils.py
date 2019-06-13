import itertools as itl

class VariableInfo:
    def __init__(self, name,vtype):
        self.name = name
        self.vmholder = None
        self.vtype = vtype

    def __eq__(self, other):
        return other.name == self.name


# a lo mejor sería buena idea hacer que se pueda instanciar una sola vez.
class Type:
    def __hash__(self):
        return hash(self.name)+hash(len(self.methods))+hash(len(self.attrs))

    def cal_height(self):
        if self.height != 0:
            return
        elif self.parent_type is None:
            self.height = 1
        else:
            self.parent_type.cal_height()
            self.height = 1 + self.parent_type.height

    def _know_its_height(self):
        return self.height != 0

    def lower_equals(self,other_type):
        '''
        Determina si el other_type es ancestro de self
        :param other_type: objeto de tipo type del cual se verifica la condición
        de ancestro.
        :return: boolean
        '''
        if other_type == self:
            return True
        if not self._know_its_height():
            self.cal_height()

        if not other_type._know_its_height():
            other_type.cal_height()

        if self.height > other_type.height:
            the_highest = self
            the_lowest = other_type
        else:
            the_highest = other_type
            the_lowest = self

        while the_highest.parent_type is not None:
            if the_highest.height == the_lowest.height:
                if the_highest != the_lowest:
                    return False
                else:
                    return True
            the_highest = the_highest.parent_type
        return False

    def __init__(self,name:str,line:int,index:int,parent_type_name='Object', node_ast_ref=None):
        '''

        :param name: Nombre de la clase
        :param attrs: diccionario {nombre_del_attr : ObjetoAttr}
        :param methods: diccionario {nombre_del_method : ObjetoMethod}
        :param parent_type: str del tipo del padre
        '''
        self.index = index
        self.line = line
        self.name = name
        self.attrs = {}
        self.methods = {}
        self._parent_type_name = parent_type_name
        self.parent_type = None
        self._checking_for_cycle = False
        self._checked_for_cycle = False
        self.height = 0
        self.updated_attrs_inheritence = False
        self.node_ast_ref = node_ast_ref

    def __eq__(self, other):
        return isinstance(other,Type) and other.name == self.name

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
        try:
            method = self.methods[name]
            return method
        except KeyError:
            return None

    def get_lca(self, other_type):
        list_of_types = set()
        object_obj = classes_dictionary['Object']
        while other_type != object_obj:
            # print('object class',object_obj,' othertype',other_type)
            list_of_types.add(other_type)
            other_type = other_type.parent_type
            # print('object class', object_obj, ' othertype', other_type)
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
        if self._parent_type_name in context.scope_classes_dictionary:
            self.parent_type = context.scope_classes_dictionary[self._parent_type_name]
            return True
        return False

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


Str_Class = Type('String',line=0,index=0)
Bool_Class = Type("Bool",line=0,index=0)
Bool_Class.updated_attrs_inheritence = True
Int_Class = Type("Int",line=0,index=0)
Int_Class.updated_attrs_inheritence = True
Object_Class = Type('Object',parent_type_name=None,line=0,index=0)
IO_Class = Type("IO", line=0, index=0)

builtins_classes = {Str_Class, Bool_Class, Int_Class, Object_Class, IO_Class}
builtins_classes_names = {Str_Class.name, Bool_Class.name, Int_Class.name, Object_Class.name, IO_Class.name}

Str_Class.parent_type = Object_Class
Bool_Class.parent_type = Object_Class
Int_Class.parent_type = Object_Class
IO_Class.parent_type = Object_Class


Str_Class.define_method('length',Int_Class)
Str_Class.define_method('concat',Str_Class, [('s',Str_Class)])
Str_Class.define_method('substr',Str_Class, [('i',Int_Class),('l',Int_Class)])
Str_Class.updated_attrs_inheritence = True

IO_Class.define_method('out_string',IO_Class,[('x',Str_Class)])
IO_Class.define_method('out_int',IO_Class,[('x',Int_Class)])
IO_Class.define_method('in_string',Str_Class)
IO_Class.define_method('in_int',Int_Class)
IO_Class.updated_attrs_inheritence = True

# el metodo copy oficialmente devuelve un SELF_TYPE pero devolveremos un object type
Object_Class.define_method('copy',Object_Class)
Object_Class.define_method('abort',Object_Class)
Object_Class.define_method('type_name',Object_Class)
Object_Class.updated_attrs_inheritence = True
# en este diccionario se va a mapear el nombre del tipo
# a la instancia del mismo que contendrá todos sus metodos y attributos
classes_dictionary = {'Int': Int_Class,
                      'String': Str_Class,
                      'Bool': Bool_Class,
                      'Object': Object_Class,
                      'IO': IO_Class
                      }


class Scope:

    scope_classes_dictionary = classes_dictionary

    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index_at_parent = 0 if parent is None else len(parent.locals)

    def define_variable(self, vname, vtypename):
        '''
        Salva vinfo (vname,vtype) en la lista locals
        :param vname:
        :param vtypename:
        :return:
        '''
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

    def type_is_defined(self,type_name):
        return self.get_type(type_name)

    def _classes_global_field(self):
        return self.scope_classes_dictionary


    @staticmethod
    def find_variable_info(vname, scope, top=None):
        if top is None:
            top = len(scope.locals)
        candidates = (vinfo for vinfo in itl.islice(scope.locals, top) if vinfo.name == vname)
        return next(candidates, None)

    def get_type(self, typeName):
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
        pass

    def create_type(self, name, inherit_type_name, line, index,node_ast_ref):
        new_type = Type(name, line=line, index=index, parent_type_name=inherit_type_name,node_ast_ref=node_ast_ref)
        self.scope_classes_dictionary[name] = new_type

    def get_params_from_method(self, type_name, method_name):
        try:
            thetype = self.scope_classes_dictionary[type_name]
        except KeyError:
            return None

        if method_name in thetype.methods:
            return thetype.methods[method_name]
        elif thetype.name != 'Object':
            return self.get_params_from_method(thetype._parent_type_name,method_name)
        return None

    def get_type_from_attr(self,type_name,attr_name):
        thetype = self.scope_classes_dictionary[type_name]
        if thetype is None:
            return None

        if attr_name in thetype.attrs:
            return thetype.attrs[attr_name]
        return None

    def get_method_from_type(self, typeName, method_name):
        type = self.get_type(typeName)
        if type is None:
            return None
        return type.get_method(method_name)

